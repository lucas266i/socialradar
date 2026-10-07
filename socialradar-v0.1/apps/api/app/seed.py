from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from .main import engine, Base, Profile, Thread

Base.metadata.create_all(engine)

now = datetime.now(timezone.utc)

profiles = [
    Profile(username="ana_ai", name="Ana Torres", bio="AI Engineer | Building agents and developer tools", country="Colombia", language="es", followers=18400, following=900, website="https://example.com/ana", youtube="https://youtube.com/", github="https://github.com/", telegram=None, linkedin="https://linkedin.com/", last_post_at=now-timedelta(days=2), last_activity_at=now-timedelta(days=1), posts_30d=22, replies_30d=31, reposts_30d=14),
    Profile(username="dev_mateo", name="Mateo Ruiz", bio="Software Engineer | Android | Kotlin | Open Source", country="Colombia", language="es", followers=9200, following=600, website="https://example.com/mateo", youtube=None, github="https://github.com/", telegram="https://t.me/", linkedin=None, last_post_at=now-timedelta(days=4), last_activity_at=now-timedelta(days=3), posts_30d=18, replies_30d=24, reposts_30d=9),
    Profile(username="ml_researcher", name="Laura Chen", bio="ML researcher | LLMs | RAG | Agents | Research notes", country="United States", language="en", followers=121000, following=1200, website="https://example.com/laura", youtube="https://youtube.com/", github="https://github.com/", telegram=None, linkedin="https://linkedin.com/", last_post_at=now-timedelta(days=7), last_activity_at=now-timedelta(days=2), posts_30d=15, replies_30d=18, reposts_30d=42),
    Profile(username="startup_lab", name="Carlos Mendes", bio="Founder | SaaS | Startups | AI products", country="Brazil", language="pt", followers=53000, following=1800, website="https://example.com/carlos", youtube="https://youtube.com/", github=None, telegram="https://t.me/", linkedin="https://linkedin.com/", last_post_at=now-timedelta(days=12), last_activity_at=now-timedelta(days=10), posts_30d=9, replies_30d=12, reposts_30d=8),
    Profile(username="old_account", name="Old Account", bio="Engineer and technology writer", country="Spain", language="es", followers=88000, following=500, website="https://example.com/old", youtube=None, github=None, telegram=None, linkedin=None, last_post_at=now-timedelta(days=210), last_activity_at=now-timedelta(days=210), posts_30d=0, replies_30d=0, reposts_30d=0),
]

threads = [
    Thread(author_username="ana_ai", title="Cómo pensar un agente de IA desde cero", topic="AI", language="es", body="Una guía práctica para entender agentes, herramientas, memoria, planificación y evaluación.", post_count=18, likes=4200, reposts=910, replies=180, created_at=now-timedelta(days=3)),
    Thread(author_username="ml_researcher", title="RAG no es solamente buscar documentos", topic="AI", language="en", body="A practical explanation of retrieval, ranking, context construction and evaluation.", post_count=21, likes=8700, reposts=2200, replies=430, created_at=now-timedelta(days=6)),
    Thread(author_username="dev_mateo", title="10 errores comunes al crear apps Android modernas", topic="Android", language="es", body="Arquitectura, estado, permisos, rendimiento y errores de compilación.", post_count=14, likes=1800, reposts=390, replies=90, created_at=now-timedelta(days=11)),
    Thread(author_username="startup_lab", title="Cómo validar una idea SaaS sin gastar dinero", topic="Startups", language="pt", body="Proceso paso a paso para validar demanda antes de construir.", post_count=12, likes=3200, reposts=760, replies=140, created_at=now-timedelta(days=16)),
]

with Session(engine) as db:
    db.query(Profile).delete()
    db.query(Thread).delete()
    db.add_all(profiles)
    db.add_all(threads)
    db.commit()

print("Seed completed.")
