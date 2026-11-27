# AGENTS.md — Project Context & CLI Handoff Guide

## Project Goal
Rebuild `DeepImageSearch_with_django` (originally a minimal Django 3.2 + VGG16 + Annoy prototype) into an **interview-grade, mobile-first Visual Product Search & High-Concurrency Commerce Platform**, designed with **AI Inference Infrastructure** rigor (comparable to production LLM/Vision inference system design: back-of-the-envelope sizing, quantization/caching, dynamic micro-batching, compute/memory stage disaggregation, data parallelism, and reproducible benchmarks).

## Current Status & Handoff
- **Active Branch:** `v2/visual-commerce`
- **Completed Design Work:**
  - Full system architecture, back-of-the-envelope math, edge–cloud balancing, and failure-mode analysis documented in `docs/SYSTEM_DESIGN.md` (`docs/SYSTEM_DESIGN.zh-TW.md`).
  - Modular 7-part component breakdown & priority roadmap documented in `docs/ROADMAP.md` (`docs/ROADMAP.zh-TW.md`).
  - **Part 0 (`infra-foundation`)** design interview completed and tracked in **GitHub Issue #1**: https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1 (detailed spec in `docs/specs/part-0-infra-foundation.md`).
- **Immediate Next Steps (pick either):**
  1. **Implement Issue #1 (`Part 0`)** on `v2/visual-commerce` following `docs/specs/part-0-infra-foundation.md`.
  2. Run a design interview (`/grill-me`) on **Part 1 (`vision-inference`)** before opening Issue #2.

## Locked-in Engineering Conventions
- **Git & Legacy Preservation:** Keep original v1 code under `legacy/` on `v2/visual-commerce` for before-vs-after interview comparison; remove `.idea/` tracking in v2.
- **Monorepo Layout (to be scaffolded in Part 0):**
  - `services/commerce/` — Django 5 + DRF commerce API + isolated background worker entrypoint (sharing Django ORM).
  - `services/vision/` — FastAPI (ASGI) ONNX/SigLIP inference & WebSocket streaming gateway.
  - `packages/contracts/` — Shared Pydantic v2 schemas for HTTP & WebSocket contracts.
  - `frontend/` — Mobile-first PWA camera viewfinder & bottom-sheet shopping UI.
  - `benchmarks/` — Locust/k6 load tests & fault-injection scripts.
  - `docs/` — Bilingual documentation.
  - `legacy/` — Original v1 codebase.
- **Infrastructure & Hardware:**
  - Local dev has **NVIDIA GPU** (Linux/Windows Docker GPU passthrough). Provide CPU-default `docker-compose.yml` (CI-friendly) + `docker-compose.gpu.yml` override.
  - Gateway: **Caddy** internal reverse proxy + optional `--profile tunnel` running **`cloudflared`** (`CLOUDFLARE_TUNNEL_TOKEN`) for trusted HTTPS / `wss://` on the owner's Cloudflare domain (required for mobile iOS Safari / Android Chrome camera access).
  - Object Storage: S3-compatible interface defaulting to local **MinIO**, switchable to **Cloudflare R2** purely via `.env`.
  - Event Queue / Checkpoints: **PostgreSQL State Machine (`BatchJob` + `lease_until`) + Redis Streams** behind a pluggable `EventBroker` interface (lightweight default; cleanly swappable to RocketMQ/Kafka if scaled 100x). Never route live camera search through a durable FIFO MQ.
- **Python Tooling:** `uv` workspace (`pyproject.toml`), `ruff` (lint + format), `pytest`, GitHub Actions CI.
- **Language Policy:**
  - Code, GitHub Issues, PRs, Commits, and default Markdown docs (`README.md`, `docs/*.md`): **English**.
  - Maintain Traditional Chinese companion docs (`README.zh-TW.md`, `docs/*.zh-TW.md`) with a top-of-page bilingual switcher.
