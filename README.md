[README.md](https://github.com/user-attachments/files/33167050/README.md)
# SocialRadar V0.1

Motor de descubrimiento de perfiles y hilos públicos. V0.1 funciona sin APIs externas:
- PostgreSQL
- FastAPI
- Next.js
- datos de demostración
- búsqueda de perfiles
- filtros por seguidores, país, idioma, tema y actividad
- búsqueda de hilos
- ranking básico
- enlaces externos detectados

## Requisitos
- Docker + Docker Compose
- Node.js 20+
- Python 3.11+

## Arranque rápido

### 1. Base de datos
```bash
docker compose up -d db
```

### 2. Backend
```bash
cd apps/api
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Seed
En otra terminal:
```bash
cd apps/api
python -m app.seed
```

### 4. Frontend
```bash
cd apps/web
npm install
npm run dev
```

Abrir:
http://localhost:3000

API:
http://localhost:8000/docs

## Próxima fase
Sustituir el proveedor demo por un adaptador de X API sin cambiar el buscador ni la base de datos.
