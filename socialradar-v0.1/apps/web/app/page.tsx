 "use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Profile = {
  username: string; name: string; bio: string; country: string;
  language: string; followers: number; last_activity_at: string;
  activity_age_days: number; posts_30d: number; replies_30d: number;
  reposts_30d: number; website?: string; youtube?: string;
  telegram?: string; github?: string; linkedin?: string;
};

type Thread = {
  id: number; author_username: string; title: string; topic: string;
  language: string; body: string; post_count: number; likes: number;
  reposts: number; replies: number; created_at: string; score: number;
};

export default function Home() {
  const [section, setSection] = useState<"profiles" | "threads">("profiles");
  const [q, setQ] = useState("");
  const [country, setCountry] = useState("");
  const [language, setLanguage] = useState("");
  const [minFollowers, setMinFollowers] = useState("");
  const [maxFollowers, setMaxFollowers] = useState("");
  const [activeDays, setActiveDays] = useState("30");
  const [days, setDays] = useState("30");
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [loading, setLoading] = useState(false);

  async function search() {
    setLoading(true);
    try {
      if (section === "profiles") {
        const params = new URLSearchParams({
          q, country, language,
          min_followers: minFollowers || "0",
          max_followers: maxFollowers || "2000000000",
          active_days: activeDays || "0",
          limit: "100"
        });
        const r = await fetch(`${API}/profiles?${params}`);
        const data = await r.json();
        setProfiles(data.results || []);
      } else {
        const params = new URLSearchParams({ q, language, days, limit: "100" });
        const r = await fetch(`${API}/threads?${params}`);
        const data = await r.json();
        setThreads(data.results || []);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { search(); }, [section]);

  return (
    <main>
      <header className="top">
        <div>
          <div className="brand">SocialRadar</div>
          <div className="subtitle">Descubre perfiles, creadores y mejores hilos.</div>
        </div>
        <span className="badge">V0.1 • DEMO</span>
      </header>

      <nav className="tabs">
        <button className={section === "profiles" ? "active" : ""} onClick={() => setSection("profiles")}>🔎 Perfiles</button>
        <button className={section === "threads" ? "active" : ""} onClick={() => setSection("threads")}>🧵 Mejores hilos</button>
      </nav>

      <section className="searchbox">
        <input value={q} onChange={e => setQ(e.target.value)} placeholder={section === "profiles" ? "Bio, nombre, usuario o palabra clave..." : "Tema, palabra o título del hilo..."} />
        {section === "profiles" && <>
          <input value={country} onChange={e => setCountry(e.target.value)} placeholder="País (ej. Colombia)" />
          <select value={language} onChange={e => setLanguage(e.target.value)}>
            <option value="">Todos los idiomas</option><option value="es">Español</option><option value="en">English</option><option value="pt">Português</option>
          </select>
          <input value={minFollowers} onChange={e => setMinFollowers(e.target.value)} placeholder="Seguidores mín." type="number" />
          <input value={maxFollowers} onChange={e => setMaxFollowers(e.target.value)} placeholder="Seguidores máx." type="number" />
          <select value={activeDays} onChange={e => setActiveDays(e.target.value)}>
            <option value="15">Activo 15 días</option><option value="30">Activo 30 días</option><option value="60">Activo 60 días</option><option value="90">Activo 90 días</option><option value="180">Activo 180 días</option><option value="0">Sin filtro de actividad</option>
          </select>
        </>}
        {section === "threads" && <select value={days} onChange={e => setDays(e.target.value)}>
          <option value="7">Últimos 7 días</option><option value="30">Últimos 30 días</option><option value="90">Últimos 90 días</option><option value="180">Últimos 180 días</option><option value="0">Todo</option>
        </select>}
        <button className="search" onClick={search}>{loading ? "Buscando..." : "Buscar"}</button>
      </section>

      {section === "profiles" ? (
        <section className="grid">
          {profiles.map(p => (
            <article className="card" key={p.username}>
              <div className="row"><strong>{p.name}</strong><span className="green">● {p.activity_age_days === 0 ? "hoy" : `hace ${p.activity_age_days} días`}</span></div>
              <div className="handle">@{p.username}</div>
              <p>{p.bio}</p>
              <div className="stats"><span>👥 {p.followers.toLocaleString()}</span><span>📝 {p.posts_30d} posts/30d</span><span>💬 {p.replies_30d}</span><span>🔁 {p.reposts_30d}</span></div>
              <div className="meta">🌎 {p.country || "—"} · 🗣 {p.language || "—"}</div>
              <div className="links">
                {p.website && <a href={p.website} target="_blank">🌐 Web</a>}
                {p.youtube && <a href={p.youtube} target="_blank">▶ YouTube</a>}
                {p.telegram && <a href={p.telegram} target="_blank">✈ Telegram</a>}
                {p.github && <a href={p.github} target="_blank">🐙 GitHub</a>}
              </div>
            </article>
          ))}
        </section>
      ) : (
        <section className="threads">
          {threads.map((t, i) => (
            <article className="thread" key={t.id}>
              <div className="rank">#{i + 1}</div>
              <div>
                <div className="threadhead"><span>🧵</span><strong>{t.title}</strong></div>
                <div className="handle">@{t.author_username} · {t.topic} · {t.language}</div>
                <p>{t.body}</p>
                <div className="stats"><span>❤️ {t.likes.toLocaleString()}</span><span>🔁 {t.reposts.toLocaleString()}</span><span>💬 {t.replies.toLocaleString()}</span><span>🧵 {t.post_count} posts</span></div>
              </div>
            </article>
          ))}
        </section>
      )}

      <footer>SocialRadar V0.1 — datos de demostración. X API se conectará mediante un adaptador en la siguiente fase.</footer>
    </main>
  );
}
