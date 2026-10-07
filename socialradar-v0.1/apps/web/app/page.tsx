"use client";

import { useCallback, useEffect, useState } from "react";

const API = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

type Profile = {
  username: string;
  name: string;
  bio: string;
  country?: string | null;
  language?: string | null;
  followers: number;
  last_activity_at?: string | null;
  activity_age_days?: number | null;
  posts_30d: number;
  replies_30d: number;
  reposts_30d: number;
  website?: string | null;
  youtube?: string | null;
  telegram?: string | null;
  github?: string | null;
  linkedin?: string | null;
};

type Thread = {
  id: number;
  author_username: string;
  title: string;
  topic: string;
  language?: string | null;
  body: string;
  post_count: number;
  likes: number;
  reposts: number;
  replies: number;
  created_at: string;
  score: number;
};

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

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
  const [error, setError] = useState("");

  const search = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      if (section === "profiles") {
        const params = new URLSearchParams({
          q,
          country,
          language,
          min_followers: minFollowers || "0",
          max_followers: maxFollowers || "2000000000",
          active_days: activeDays || "0",
          limit: "100",
        });
        const data = await getJson<{ results?: Profile[] }>(`${API}/profiles?${params}`);
        setProfiles(data.results || []);
      } else {
        const params = new URLSearchParams({
          q,
          language,
          days,
          limit: "100",
        });
        const data = await getJson<{ results?: Thread[] }>(`${API}/threads?${params}`);
        setThreads(data.results || []);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo conectar con la API.");
      if (section === "profiles") setProfiles([]);
      else setThreads([]);
    } finally {
      setLoading(false);
    }
  }, [section, q, country, language, minFollowers, maxFollowers, activeDays, days]);

  useEffect(() => {
    void search();
  }, [search]);

  return (
    <main>
      <header className="top">
        <div>
          <div className="brand">SocialRadar</div>
          <div className="subtitle">Descubre perfiles, creadores y mejores hilos.</div>
        </div>
        <span className="badge">V0.1 • DEMO</span>
      </header>

      <nav className="tabs" aria-label="Secciones">
        <button
          className={section === "profiles" ? "active" : ""}
          onClick={() => setSection("profiles")}
          type="button"
        >
          🔎 Perfiles
        </button>
        <button
          className={section === "threads" ? "active" : ""}
          onClick={() => setSection("threads")}
          type="button"
        >
          🧵 Mejores hilos
        </button>
      </nav>

      <section className="searchbox">
        <input
          value={q}
          onChange={(event) => setQ(event.target.value)}
          placeholder={
            section === "profiles"
              ? "Bio, nombre, usuario o palabra clave..."
              : "Tema, palabra o título del hilo..."
          }
          aria-label="Buscar"
        />

        {section === "profiles" && (
          <>
            <input
              value={country}
              onChange={(event) => setCountry(event.target.value)}
              placeholder="País (ej. Colombia)"
              aria-label="País"
            />
            <select value={language} onChange={(event) => setLanguage(event.target.value)} aria-label="Idioma">
              <option value="">Todos los idiomas</option>
              <option value="es">Español</option>
              <option value="en">English</option>
              <option value="pt">Português</option>
            </select>
            <input
              value={minFollowers}
              onChange={(event) => setMinFollowers(event.target.value)}
              placeholder="Seguidores mín."
              type="number"
              min="0"
              aria-label="Seguidores mínimos"
            />
            <input
              value={maxFollowers}
              onChange={(event) => setMaxFollowers(event.target.value)}
              placeholder="Seguidores máx."
              type="number"
              min="0"
              aria-label="Seguidores máximos"
            />
            <select value={activeDays} onChange={(event) => setActiveDays(event.target.value)} aria-label="Actividad">
              <option value="15">Activo 15 días</option>
              <option value="30">Activo 30 días</option>
              <option value="60">Activo 60 días</option>
              <option value="90">Activo 90 días</option>
              <option value="180">Activo 180 días</option>
              <option value="0">Sin filtro de actividad</option>
            </select>
          </>
        )}

        {section === "threads" && (
          <select value={days} onChange={(event) => setDays(event.target.value)} aria-label="Antigüedad">
            <option value="7">Últimos 7 días</option>
            <option value="30">Últimos 30 días</option>
            <option value="90">Últimos 90 días</option>
            <option value="180">Últimos 180 días</option>
            <option value="0">Todo</option>
          </select>
        )}

        <button className="search" onClick={() => void search()} disabled={loading} type="button">
          {loading ? "Buscando..." : "Buscar"}
        </button>
      </section>

      {error && (
        <div className="error" role="alert">
          {error}. Verifica que la API esté ejecutándose en {API}.
        </div>
      )}

      {section === "profiles" ? (
        <section className="grid">
          {!loading && profiles.length === 0 && !error && <div className="empty">No hay perfiles que coincidan.</div>}
          {profiles.map((profile) => (
            <article className="card" key={profile.username}>
              <div className="row">
                <strong>{profile.name}</strong>
                <span className="green">
                  ● {profile.activity_age_days == null
                    ? "sin actividad"
                    : profile.activity_age_days === 0
                      ? "hoy"
                      : `hace ${profile.activity_age_days} días`}
                </span>
              </div>
              <div className="handle">@{profile.username}</div>
              <p>{profile.bio}</p>
              <div className="stats">
                <span>👥 {profile.followers.toLocaleString()}</span>
                <span>📝 {profile.posts_30d} posts/30d</span>
                <span>💬 {profile.replies_30d}</span>
                <span>🔁 {profile.reposts_30d}</span>
              </div>
              <div className="meta">
                🌎 {profile.country || "—"} · 🗣 {profile.language || "—"}
              </div>
              <div className="links">
                {profile.website && <a href={profile.website} target="_blank" rel="noreferrer">🌐 Web</a>}
                {profile.youtube && <a href={profile.youtube} target="_blank" rel="noreferrer">▶ YouTube</a>}
                {profile.telegram && <a href={profile.telegram} target="_blank" rel="noreferrer">✈ Telegram</a>}
                {profile.github && <a href={profile.github} target="_blank" rel="noreferrer">🐙 GitHub</a>}
                {profile.linkedin && <a href={profile.linkedin} target="_blank" rel="noreferrer">in LinkedIn</a>}
              </div>
            </article>
          ))}
        </section>
      ) : (
        <section className="threads">
          {!loading && threads.length === 0 && !error && <div className="empty">No hay hilos que coincidan.</div>}
          {threads.map((thread, index) => (
            <article className="thread" key={thread.id}>
              <div className="rank">#{index + 1}</div>
              <div>
                <div className="threadhead">
                  <span>🧵</span>
                  <strong>{thread.title}</strong>
                </div>
                <div className="handle">
                  @{thread.author_username} · {thread.topic} · {thread.language || "—"}
                </div>
                <p>{thread.body}</p>
                <div className="stats">
                  <span>❤️ {thread.likes.toLocaleString()}</span>
                  <span>🔁 {thread.reposts.toLocaleString()}</span>
                  <span>💬 {thread.replies.toLocaleString()}</span>
                  <span>🧵 {thread.post_count} posts</span>
                </div>
              </div>
            </article>
          ))}
        </section>
      )}

      <footer>
        SocialRadar V0.1 — datos de demostración. La integración con X deberá usar un adaptador oficial en una fase posterior.
      </footer>
    </main>
  );
}
