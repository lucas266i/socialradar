from datetime import datetime, timedelta, timezone
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, create_engine, inspect, or_, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://socialradar:socialradar@localhost:5432/socialradar",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    bio: Mapped[str] = mapped_column(Text())
    country: Mapped[str | None] = mapped_column(String(100), index=True)
    language: Mapped[str | None] = mapped_column(String(50), index=True)
    followers: Mapped[int] = mapped_column(Integer, index=True)
    following: Mapped[int] = mapped_column(Integer, default=0)
    website: Mapped[str | None] = mapped_column(String(500))
    youtube: Mapped[str | None] = mapped_column(String(500))
    telegram: Mapped[str | None] = mapped_column(String(500))
    github: Mapped[str | None] = mapped_column(String(500))
    linkedin: Mapped[str | None] = mapped_column(String(500))
    last_post_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    posts_30d: Mapped[int] = mapped_column(Integer, default=0)
    replies_30d: Mapped[int] = mapped_column(Integer, default=0)
    reposts_30d: Mapped[int] = mapped_column(Integer, default=0)


class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_username: Mapped[str] = mapped_column(String(100), index=True)
    author_profile_id: Mapped[int | None] = mapped_column(ForeignKey("profiles.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    topic: Mapped[str] = mapped_column(String(200), index=True)
    language: Mapped[str | None] = mapped_column(String(50), index=True)
    body: Mapped[str] = mapped_column(Text())
    post_count: Mapped[int] = mapped_column(Integer, default=1)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    reposts: Mapped[int] = mapped_column(Integer, default=0)
    replies: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


app = FastAPI(title="SocialRadar API", version="0.1.1")

origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ensure_compatible_schema() -> None:
    """Apply only additive compatibility changes for existing demo databases."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "threads" in tables:
        columns = {column["name"] for column in inspector.get_columns("threads")}
        if "author_profile_id" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE threads "
                        "ADD COLUMN IF NOT EXISTS author_profile_id INTEGER "
                        "REFERENCES profiles(id) ON DELETE SET NULL"
                    )
                )
                connection.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS ix_threads_author_profile_id "
                        "ON threads(author_profile_id)"
                    )
                )

Base.metadata.create_all(engine)
ensure_compatible_schema()


def utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def profile_dict(profile: Profile) -> dict:
    now = datetime.now(timezone.utc)
    last_activity = utc(profile.last_activity_at)
    age_days = None
    if last_activity:
        age_days = max(0, (now - last_activity).days)

    return {
        "id": profile.id,
        "username": profile.username,
        "name": profile.name,
        "bio": profile.bio,
        "country": profile.country,
        "language": profile.language,
        "followers": profile.followers,
        "following": profile.following,
        "website": profile.website,
        "youtube": profile.youtube,
        "telegram": profile.telegram,
        "github": profile.github,
        "linkedin": profile.linkedin,
        "last_post_at": profile.last_post_at,
        "last_activity_at": profile.last_activity_at,
        "activity_age_days": age_days,
        "posts_30d": profile.posts_30d,
        "replies_30d": profile.replies_30d,
        "reposts_30d": profile.reposts_30d,
    }


def thread_dict(thread: Thread) -> dict:
    return {
        "id": thread.id,
        "author_username": thread.author_username,
        "author_profile_id": thread.author_profile_id,
        "title": thread.title,
        "topic": thread.topic,
        "language": thread.language,
        "body": thread.body,
        "post_count": thread.post_count,
        "likes": thread.likes,
        "reposts": thread.reposts,
        "replies": thread.replies,
        "created_at": thread.created_at,
        "score": thread.likes + thread.reposts * 2 + thread.replies,
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": app.version}


@app.get("/profiles")
def profiles(
    q: str = "",
    country: str = "",
    language: str = "",
    min_followers: int = Query(0, ge=0),
    max_followers: int = Query(2_000_000_000, ge=0),
    active_days: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
):
    if min_followers > max_followers:
        raise HTTPException(status_code=400, detail="min_followers cannot exceed max_followers")

    with Session(engine) as db:
        stmt = select(Profile)
        if q.strip():
            term = f"%{q.strip().lower()}%"
            stmt = stmt.where(
                or_(
                    Profile.bio.ilike(term),
                    Profile.name.ilike(term),
                    Profile.username.ilike(term),
                )
            )
        if country.strip():
            stmt = stmt.where(Profile.country == country.strip())
        if language.strip():
            stmt = stmt.where(Profile.language == language.strip())

        stmt = stmt.where(
            Profile.followers >= min_followers,
            Profile.followers <= max_followers,
        )

        if active_days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=active_days)
            stmt = stmt.where(Profile.last_activity_at >= cutoff)

        stmt = stmt.order_by(
            (Profile.posts_30d + Profile.replies_30d + Profile.reposts_30d).desc(),
            Profile.followers.desc(),
        )

        rows = list(db.scalars(stmt.limit(limit)).all())
        return {"count": len(rows), "results": [profile_dict(profile) for profile in rows]}


@app.get("/profiles/{username}")
def profile(username: str):
    with Session(engine) as db:
        profile = db.scalar(select(Profile).where(Profile.username.ilike(username)))
        if not profile:
            raise HTTPException(status_code=404, detail="profile_not_found")
        return profile_dict(profile)


@app.get("/threads")
def threads(
    q: str = "",
    topic: str = "",
    language: str = "",
    days: int = Query(30, ge=0),
    limit: int = Query(50, ge=1, le=500),
):
    with Session(engine) as db:
        stmt = select(Thread)
        if q.strip():
            term = f"%{q.strip().lower()}%"
            stmt = stmt.where(
                or_(
                    Thread.title.ilike(term),
                    Thread.body.ilike(term),
                    Thread.topic.ilike(term),
                )
            )
        if topic.strip():
            stmt = stmt.where(Thread.topic == topic.strip())
        if language.strip():
            stmt = stmt.where(Thread.language == language.strip())
        if days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            stmt = stmt.where(Thread.created_at >= cutoff)

        rows = list(
            db.scalars(
                stmt.order_by(
                    (Thread.likes + Thread.reposts * 2 + Thread.replies).desc(),
                    Thread.created_at.desc(),
                ).limit(limit)
            ).all()
        )
        return {"count": len(rows), "results": [thread_dict(thread) for thread in rows]}
