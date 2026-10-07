# SocialRadar

Motor de descubrimiento de perfiles y hilos públicos.

La aplicación actual es una demo autocontenida con PostgreSQL, FastAPI y Next.js. No requiere APIs externas para funcionar.

## Estructura

El código de la aplicación está dentro de `socialradar-v0.1/`.

## Requisitos

- Docker + Docker Compose
- Node.js 20+
- Python 3.11+

## Arranque

### 1. Base de datos

Desde la raíz del repositorio:

```bash
cd socialradar-v0.1
docker compose up -d db
```

### 2. Backend

En otra terminal, desde la raíz:

```bash
cd socialradar-v0.1/apps/api
python -m venv .venv
```

Windows:
```bat
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instalar dependencias y arrancar:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Datos de demostración

En otra terminal:

```bash
cd socialradar-v0.1/apps/api
python -m app.seed
```

### 4. Frontend

En otra terminal:

```bash
cd socialradar-v0.1/apps/web
npm install
npm run dev
```

Abrir http://localhost:3000.

API: http://localhost:8000/docs

### API en otro dominio

Define `NEXT_PUBLIC_API_URL` en el frontend y `CORS_ORIGINS` en el backend. Ejemplo:

```text
NEXT_PUBLIC_API_URL=https://api.example.com
CORS_ORIGINS=https://socialradar.example.com
```

## Estado

V0.1 funciona con datos de demostración. La integración futura con X debe implementarse mediante un adaptador oficial, sin acoplar el frontend al proveedor.
