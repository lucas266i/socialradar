# SocialRadar

Motor de descubrimiento de perfiles y hilos públicos.

La aplicación actual es una demo autocontenida con PostgreSQL, FastAPI y Next.js. No requiere APIs externas para funcionar.

## Estructura

El código de la aplicación está dentro de `socialradar-v0.1/`.

## Requisitos

- Docker + Docker Compose
- Node.js 20.9+
- Python 3.11+

## Arranque local

### 1. Base de datos

Desde la raíz del repositorio:

```bash
cd socialradar-v0.1
docker compose up -d db
```

### 2. Backend

En otra terminal:

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

Instalar y arrancar:

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

## Variables de entorno

Backend:

- `DATABASE_URL`: conexión PostgreSQL.
- `CORS_ORIGINS`: orígenes permitidos separados por coma.

Frontend:

- `NEXT_PUBLIC_API_URL`: URL pública de la API.

## Arranque con Docker

Desde `socialradar-v0.1/`:

```bash
docker compose up --build
```

La aplicación queda disponible en `http://localhost:3000` y la API en `http://localhost:8000/docs`. El servicio `seed` carga los datos de demostración automáticamente y no borra registros ajenos a esos datos demo.

Para detener los servicios:

```bash
docker compose down
```

Para eliminar también la base de datos local:

```bash
docker compose down -v
```

## Verificación

Backend:

```bash
cd socialradar-v0.1/apps/api
python -m compileall app
```

Frontend:

```bash
cd socialradar-v0.1/apps/web
npm install
npm run build
```

## Estado

V0.1 funciona con datos de demostración. La integración futura con X debe implementarse mediante un adaptador oficial, sin acoplar el frontend al proveedor.
