# Spec: Part 0 — `infra-foundation`

- **GitHub Issue:** [#1](https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1)
- **Branch:** `v2/visual-commerce`
- **Status:** Locked & Ready for Implementation

---

## 1. Objectives
Build a clean, reproducible, CI-verified monorepo foundation supporting both **CPU-only environments (CI / laptops)** and **local NVIDIA GPU passthrough**, with **Cloudflare Tunnel HTTPS** for real mobile phone camera testing and **S3-compatible object storage (MinIO locally / Cloudflare R2 via `.env`)**.

---

## 2. Target Directory Layout

```text
DeepImageSearch_with_django/
├── .github/workflows/ci.yml        # ruff check + format check + pytest + compose config validation
├── .env.example                    # Complete documented environment template (MinIO/R2, Tunnel, DB, Redis)
├── .gitignore                      # Python, uv, Docker, IDE (.idea/), media, models cache
├── pyproject.toml                  # uv workspace root + ruff & pytest configuration
├── docker-compose.yml              # Base CPU stack (postgres+pgvector, redis, minio, gateway, commerce, vision)
├── docker-compose.gpu.yml          # NVIDIA GPU passthrough override for services/vision
├── infra/
│   ├── caddy/Caddyfile             # Internal reverse proxy: /api/* -> commerce, /ws/* & /vision/* -> vision, / -> frontend
│   └── postgres/init.sql           # CREATE EXTENSION IF NOT EXISTS vector;
├── packages/
│   └── contracts/                  # Shared Pydantic v2 schemas (health, search, throttle, events)
│       └── pyproject.toml
├── services/
│   ├── commerce/                   # Django 5 + DRF API + isolated worker entrypoint
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── ... (minimal stub with GET /api/health/ checking DB & Redis)
│   └── vision/                     # FastAPI (ASGI) inference & WebSocket service
│       ├── pyproject.toml
│       ├── Dockerfile
│       └── ... (minimal stub with GET /vision/health reporting device CPU/CUDA)
├── frontend/                       # Placeholder mobile PWA scaffold served by Caddy at /
├── benchmarks/                     # Placeholder directory for Locust/k6 scripts
├── docs/                           # Bilingual architecture docs & specs
├── legacy/                         # Original v1 Django 3.2 + DeepImageSearch codebase (moved via git mv)
├── AGENTS.md
├── README.md                       # English default (with toggle to README.zh-TW.md)
└── README.zh-TW.md                 # Traditional Chinese companion
```

---

## 3. Infrastructure Contracts

### Caddy Routing (`infra/caddy/Caddyfile`)
- `/api/*` → `commerce:8000`
- `/admin/*` → `commerce:8000`
- `/ws/*` → `vision:8001` (WebSocket upgrade preserved)
- `/vision/*` → `vision:8001`
- `/*` → static files from `/srv/frontend` (or frontend dev container)

### Cloudflare Tunnel Profile (`--profile tunnel`)
- Service `cloudflared` (`cloudflare/cloudflared:latest`), command `tunnel --no-autoupdate run --token ${CLOUDFLARE_TUNNEL_TOKEN}`.
- In Cloudflare Zero Trust Dashboard, configure the public hostname (e.g. `visual-shop.<your-domain>`) to forward to `http://gateway:80`.
- Mobile devices access `https://visual-shop.<your-domain>` with trusted Cloudflare TLS + `wss://` WebSockets (required for iOS Safari & Android Chrome `getUserMedia`).

### Unified S3 Object Storage (`.env.example`)
```env
# Local MinIO default (switch to Cloudflare R2 by swapping these 5 vars)
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=visual-commerce-media
S3_PUBLIC_BASE_URL=http://localhost:9000/visual-commerce-media
S3_REGION=auto
```

### GPU Override (`docker-compose.gpu.yml`)
- Adds NVIDIA GPU device reservation (`driver: nvidia`, `count: 1`, `capabilities: [gpu]`) and `VISION_DEVICE=cuda` to the `vision` service.
- Usage: `docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build` (optionally add `--profile tunnel`).

### Shared Contracts & DDIA Foundations (`packages/contracts/`)
Lightweight conventions baked in from Day 1 so Parts 1–5 need zero breaking contract refactors:
- **Schema Evolution (DDIA Ch. 4):** Base Pydantic envelope (`VersionedEnvelope`) includes `schema_version: int = 1` and `model_config = ConfigDict(extra="ignore")` for forward/backward compatibility during rolling upgrades.
- **Cross-Service Header Constants (DDIA Ch. 1 & Ch. 7):** Define shared constants for `X-Request-ID` (tracing), `X-Request-Deadline-Ms` (end-to-end deadline propagation), and `Idempotency-Key` (safe checkout retries); ensure Caddy forwards these headers unchanged.

---

## 4. Acceptance Criteria
1. Original v1 files (`DIS_django/`, `search/`, `manage.py`, `requirements.txt`, original `README.md`) are moved into `legacy/` cleanly; `.idea/` is removed from git tracking on `v2/visual-commerce`.
2. `uv sync` installs workspace packages cleanly; `uv run ruff check .` and `uv run pytest` pass.
3. `docker compose up --build` boots all core services cleanly and:
   - `GET http://localhost:8080/api/health/` returns `200 OK` verifying Postgres (`pgvector` enabled) + Redis connectivity.
   - `GET http://localhost:8080/vision/health` returns `200 OK` reporting runtime & device (`cpu` or `cuda`).
   - MinIO bucket `visual-commerce-media` is auto-created on startup.
4. `docker compose -f docker-compose.yml -f docker-compose.gpu.yml config` and `docker compose --profile tunnel config` both validate with exit code `0`.
5. GitHub Actions CI (`.github/workflows/ci.yml`) runs `ruff`, `pytest`, and compose config validation.
6. Bilingual `README.md` / `README.zh-TW.md` accurately documents architecture overview, CPU/GPU/Tunnel quickstart, and roadmap links.
