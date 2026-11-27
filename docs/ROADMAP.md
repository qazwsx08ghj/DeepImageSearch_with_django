> **Language:** **English** | [繁體中文](./ROADMAP.zh-TW.md)

# Component Breakdown & Implementation Roadmap

This roadmap decomposes the v2 rebuild into **7 modular components**, ranked by **interview/system importance** alongside their **recommended implementation sequence**. Each component follows the cadence: **Design Interview (`/grill-me`) → GitHub Issue → Branch Implementation & Verification**.

---

## Priority & Tracking Matrix

| Part | Component | Priority | Core System / Interview Value | Build Order | Status | Issue |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| **Part 1** | `vision-inference` — AI Inference Engine & Dynamic Micro-Batcher | **P0 (Core)** | AI Infra heart: ONNX/TensorRT, SLA-aware micro-batching, DP scaling | #2 | Pending `/grill-me` | — |
| **Part 2** | `vector-retrieval` — Two-Stage Vector Search & Versioned Storage | **P0 (Core)** | Quantization compression, coarse+rerank, SQL pre-filtering, zero-downtime model switch | #3 | Pending `/grill-me` | — |
| **Part 3** | `stream-gateway` & `mobile-edge` — Mobile Edge Gate & Live Streaming | **P0 (Core)** | Edge–cloud balancing, Latest-Frame-Wins, closed-loop throttling, mobile PWA | #4 | Pending `/grill-me` | — |
| **Part 4** | `commerce-core` — Django 5 + DRF Shopping Loop & Oversell Protection | **P1 (High)** | Visual-to-purchase conversion, atomic stock deduction, idempotent checkout | #5 | Pending `/grill-me` | — |
| **Part 5** | `async-indexer` — Pool Isolation, Checkpoints & Batch Indexing | **P1 (High)** | Online/Offline isolation, resumable `lease_until` checkpoints, DLQ, pluggable broker | #6 | Pending `/grill-me` | — |
| **Part 6** | `observability-benchmarks` — Grafana, 5 Stress/Chaos Benchmarks & Docs | **P1 (Differentiator)** | Reproducible P99/QPS proof, batching & isolation charts, full `SYSTEM_DESIGN.md` | #7 | Pending `/grill-me` | — |
| **Part 0** | `infra-foundation` — Monorepo, Docker Compose (CPU/GPU), Tunnel & CI | **P2 (Foundation)** | One-command setup, NVIDIA GPU override, Cloudflare Tunnel HTTPS, S3/MinIO, CI | #1 | **Spec Ready / Issue Opened** | [#1](https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1) |

---

## Component Scopes & `/grill-me` Checklists

### Part 0 — `infra-foundation` (Status: Ready to Implement — [Issue #1](https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1))
- Detailed specification: [`docs/specs/part-0-infra-foundation.md`](./specs/part-0-infra-foundation.md).

### Part 1 — `vision-inference` (P0)
- **Scope:** Standalone FastAPI (ASGI) inference service loading ONNX SigLIP/OpenCLIP once, SLA-aware Dynamic Micro-Batcher (`max_batch_size`, `max_wait_ms`, deadline drop), and deterministic Benchmark Mock mode.
- **Decisions to lock in `/grill-me`:**
  1. Target vision backbone (SigLIP-Base vs OpenCLIP ViT-B/32 vs MobileCLIP) and text-encoder support for hybrid image+text queries.
  2. Micro-batcher parameters (`max_batch_size`, `max_wait_ms`, queue cap, load-shedding status codes).
  3. Internal transport protocol (HTTP/2 vs gRPC) and GPU execution provider (`CUDAExecutionProvider` / TensorRT vs CPU fallback).

### Part 2 — `vector-retrieval` (P0)
- **Scope:** PostgreSQL 16 + `pgvector` (0.8+) versioned embeddings (`model_version`), two-stage coarse (quantized HNSW) + fine rerank, iterative SQL pre-filtering (`in_stock=True`, price, category), and 2-tier Redis caching (SHA-256 image hash + `search_id` vector cache).
- **Decisions to lock in `/grill-me`:**
  1. Precision pairing (`bit` binary coarse + `halfvec` rerank vs pure `halfvec`).
  2. Multi-image-per-product aggregation strategy (`max` score vs weighted average).
  3. Hybrid image + text vector fusion weights and `Exact Match` vs `Visually Similar` confidence thresholds.

### Part 3 — `stream-gateway` & `mobile-edge` (P0)
- **Scope:** FastAPI WebSocket streaming layer (Size-1 Latest-Frame-Wins mailbox, monotonic `seq_id`, closed-loop server `throttle` hints) + mobile-first PWA camera UI (`playsInline` rear camera, `64×64` motion/blur gate, ~30 KB JPEG, 1-in-flight throttle, optional barcode fast-path, bottom-sheet product drawer).
- **Decisions to lock in `/grill-me`:**
  1. Frontend stack (vanilla lightweight ES modules/Vite vs React/Vue vs Next.js).
  2. Default scan UX (auto-keyframe + manual freeze/shutter).
  3. Whether client-side barcode fast-path and Tier 2 browser object detection ship in v1 or Phase 2.
  4. Server metric driving dynamic `throttle` signals (queue depth, P95 latency, or GPU utilization).

### Part 4 — `commerce-core` (P1)
- **Scope:** Django 5 + DRF catalog (products, multi-angle images, variants/stock), cart, atomic oversell-safe stock deduction, `Idempotency-Key` checkout, unpaid reservation release, and scan-to-order conversion analytics.
- **Decisions to lock in `/grill-me`:**
  1. Single-level `Product` vs `Product + SKU Variant`.
  2. Direct atomic deduction vs reserve-with-TTL + simulated payment webhook confirmation.
  3. Anonymous guest cart (frictionless scan-to-buy) + optional JWT auth.
  4. Demo catalog dataset selection (multi-category retail sample).

### Part 5 — `async-indexer` (P1)
- **Scope:** Isolated background indexing worker sharing Django ORM, pluggable `EventBroker` interface (default Redis Streams, swappable to RocketMQ/Kafka), `realtime` vs `bulk` channels, DB `BatchJob` + `lease_until` resumable checkpoints, conditional `image_hash` upsert, and DLQ replay.
- **Decisions to lock in `/grill-me`:**
  1. Bulk ingestion entrypoints (CLI management command, CSV/JSON upload API, Django Admin).
  2. Lease timeout, max retries, and DLQ replay workflow.
  3. Outbox table vs `transaction.on_commit` + periodic reconciliation sweep.

### Part 6 — `observability-benchmarks` (P1)
- **Scope:** Prometheus + Grafana dashboards (P50/P95/P99 latency, batch-size histogram, dropped stale frames, cache hit ratio, stream lag) + automated Locust/k6 benchmarks proving 5 key interview scenarios.
- **Decisions to lock in `/grill-me`:**
  1. Synthetic benchmark catalog scale (e.g. 100k vectors locally) and target concurrent virtual users.
  2. Load testing tool (Locust vs k6).
  3. Top 3 live demo scenarios to showcase in interviews.
