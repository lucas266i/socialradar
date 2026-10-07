from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, String, Integer, DateTime, Text, ForeignKey, select, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://socialradar:socialradar@localhost:5432/socialradar"
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
    title: Mapped[str] = mapped_column(String(500))
    topic: Mapped[str] = mapped_column(String(200), index=True)
    language: Mapped[str | None] = mapped_column(String(50), index=True)
    body: Mapped[str] = mapped_column(Text())
    post_count: Mapped[int] = mapped_column(Integer, default=1)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    reposts: Mapped[int] = mapped_column(Integer, default=0)
    replies: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

app = FastAPI(title="SocialRadar API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

def profile_dict(p: Profile):
    now = datetime.now(timezone.utc)
    age_days = None
    if p.last_activity_at:
        dt = p.last_activity_at
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age_days = max(0, (now - dt).days)
    return {
        "id": p.id, "username": p.username, "name": p.name, "bio": p.bio,
        "country": p.country, "language": p.language, "followers": p.followers,
        "following": p.following, "website": p.website, "youtube": p.youtube,
        "telegram": p.telegram, "github": p.github, "linkedin": p.linkedin,
        "last_post_at": p.last_post_at, "last_activity_at": p.last_activity_at,
        "activity_age_days": age_days, "posts_30d": p.posts_30d,
        "replies_30d": p.replies_30d, "reposts_30d": p.reposts_30d
    }

def thread_dict(t: Thread):
    return {
        "id": t.id, "author_username": t.author_username, "title": t.title,
        "topic": t.topic, "language": t.language, "body": t.body,
        "post_count": t.post_count, "likes": t.likes, "reposts": t.reposts,
        "replies": t.replies, "created_at": t.created_at,
        "score": t.likes + t.reposts * 2 + t.replies
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/profiles")
def profiles(
    q: str = "",
    country: str = "",
    language: str = "",
    min_followers: int = 0,
    max_followers: int = 2_000_000_000,
    active_days: int = 0,
    limit: int = Query(50, ge=1, le=500),
):
    with Session(engine) as db:
        stmt = select(Profile)
        if q:
            term = f"%{q.lower()}%"
            stmt = stmt.where(or_(
                Profile.bio.ilike(term),
                Profile.name.ilike(term),
                Profile.username.ilike(term),
            ))
        if country:
            stmt = stmt.where(Profile.country == country)
        if language:
            stmt = stmt.where(Profile.language == language)
        stmt = stmt.where(Profile.followers >= min_followers)
        stmt = stmt.where(Profile.followers <= max_followers)

        rows = list(db.scalars(stmt).all())
        now = datetime.now(timezone.utc)
        if active_days > 0:
            filtered = []
            for p in rows:
                if not p.last_activity_at:
                    continue
                dt = p.last_activity_at
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if now - dt <= timedelta(days=active_days):
                    filtered.append(p)
            rows = filtered

        rows.sort(key=lambda p: (
            p.posts_30d + p.replies_30d + p.reposts_30d,
            p.followers
        ), reverse=True)
        return {"count": len(rows), "results": [profile_dict(p) for p in rows[:limit]]}

@app.get("/profiles/{username}")
def profile(username: str):
    with Session(engine) as db:
        p = db.scalar(select(Profile).where(Profile.username == username))
        if not p:
            return {"error": "profile_not_found"}
        return profile_dict(p)

@app.get("/threads")
def threads(
    q: str = "",
    topic: str = "",
    language: str = "",
    days: int = 30,
    limit: int = Query(50, ge=1, le=500),
):
    with Session(engine) as db:
        stmt = select(Thread)
        if q:
            term = f"%{q.lower()}%"
            stmt = stmt.where(or_(
                Thread.title.ilike(term),
                Thread.body.ilike(term),
                Thread.topic.ilike(term),
            ))
        if topic:
            stmt = stmt.where(Thread.topic == topic)
        if language:
            stmt = stmt.where(Thread.language == language)
        if days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            stmt = stmt.where(Thread.created_at >= cutoff)

        rows = list(db.scalars(stmt).all())
        rows.sort(key=lambda t: t.likes + t.reposts * 2 + t.replies, reverse=True)
        return {"count": len(rows), "results": [thread_dict(t) for t in rows[:limit]]}
