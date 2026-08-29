# Simplex Studio

A lightweight linear programming application built with Next.js on the frontend and a Python simplex engine on the backend.

## Detected project structure

- Frontend: `frontend/` using Next.js 16 and React 19
- Backend: `backend/` using a Python `http.server` implementation, no external web framework required
- Core solver: `backend/simplex.py` via `SimplexMethod`
- Frontend runs locally on port `3000`
- Python API runs on port `8000`
- Package manager: `pnpm` via `frontend/package.json`
- Python runtime: standard library only; no additional Python packages are required for the solver/API

## Architecture

- User requests the Next.js frontend
- Frontend optionally sends requests to the Python API at `NEXT_PUBLIC_API_URL`
- Python backend runs the original simplex algorithm without changing the mathematical logic
- No database, user auth, or persistent storage

## Local development

1. Start the Python API:
   ```bash
   python backend/api_server.py
   ```
   The API listens on `http://localhost:8000/solve`.

2. Start the frontend:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```
   The frontend runs on `http://localhost:3000`.

3. Configure the frontend API URL if you want to use the backend instead of the browser fallback solver:
   ```bash
   cp .env.example .env.local
   ```
   Then set:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/solve
   ```

## Docker local development

From the project root:

```bash
docker compose up --build
```

Then open:
- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health

## Production Docker build

```bash
docker compose build
```

Then start the stack:

```bash
docker compose up -d
```

## Required environment variables

Create a `.env` file or use Docker environment injection with these values:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/solve
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

For Docker Compose, the frontend service uses `http://simplex-api:8000/solve` internally.

## Deploying to a Linux VPS

1. Copy the repository to the server.
2. Ensure Docker and Docker Compose are installed.
3. Create a `.env` file with the same variables as `.env.example`.
4. Run:
   ```bash
   docker compose up --build -d
   ```
5. Expose ports `3000` and `8000` through the server firewall or reverse proxy.

## Deploying to AWS, Azure, GCP, and DigitalOcean

This app is a standard two-service Docker deployment:
- one container for the Python API
- one container for the Next.js frontend

Deploy the same `docker-compose.yml` on a Docker-capable VM or ECS/EKS/AKS/GKE/Container Service platform, or run the containers directly on a Linux server. The design does not depend on a database or a custom platform runtime.

## Cloudflare setup

Cloudflare can be used for:
- DNS
- HTTPS certificates
- domain routing
- proxying and traffic termination

Use Cloudflare in front of the deployed frontend and/or API, but keep the Python backend in a normal container runtime. The Python backend cannot run directly as a Cloudflare Workers-native function because it relies on a standard Python runtime and container-based HTTP server.

The simplest Cloudflare pattern is:
- Cloudflare points your domain to your host or load balancer
- HTTPS is terminated by Cloudflare
- traffic is forwarded to the Docker host running the frontend and backend containers

## Summary

This project remains intentionally simple:
- no database
- no auth
- no persistent storage
- no unnecessary services
- only a frontend and a backend service

The mathematical solver remains unchanged.
