> **語言：** [English](./ROADMAP.md) | **繁體中文**

# 系統部件拆分、重要性排序與開發路線圖

本路線圖將 v2 重構拆分為 **7 個獨立模組**，同時標註 **面試／架構重要性（Priority）** 與 **建議實作順序**。每個部件依循固定節奏推進：**深度對齊（`/grill-me`）→ 開立 GitHub Issue → 分支實作與測試驗收**。

---

## 重要性排序與追蹤總表

| 部件 | 名稱 | 重要性 | 核心系統與面試價值 | 建議實作順序 | 狀態 | Issue |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| **Part 1** | `vision-inference` — AI 推論引擎與 Dynamic Micro-Batcher | **P0 (最高)** | AI Infra 核心：ONNX/TensorRT、SLA 動態合批、純 DP 擴充 | #2 | 待 `/grill-me` | — |
| **Part 2** | `vector-retrieval` — 兩階段向量檢索與版本化儲存 | **P0 (最高)** | 量化壓縮、粗排＋精排、SQL 庫存預過濾、零停機換模型 | #3 | 待 `/grill-me` | — |
| **Part 3** | `stream-gateway` & `mobile-edge` — 手機閘門與即時串流 | **P0 (最高)** | 邊雲算力平衡、Latest-Frame-Wins、閉環降頻、手機 PWA | #4 | 待 `/grill-me` | — |
| **Part 4** | `commerce-core` — Django 5 + DRF 商務閉環與防超賣 | **P1 (高)** | 視覺導購落地消費、原子扣庫存、冪等即時結帳 | #5 | 待 `/grill-me` | — |
| **Part 5** | `async-indexer` — 資源隔離、斷點續傳與批次建索引 | **P1 (高)** | Online/Offline 隔離、`lease_until` 斷點續傳、DLQ、可抽換 Broker | #6 | 待 `/grill-me` | — |
| **Part 6** | `observability-benchmarks` — Grafana、5 大壓測與設計書 | **P1 (決勝)** | 可重現 P99/QPS 數據、合批與隔離實測圖表、完整設計書 | #7 | 待 `/grill-me` | — |
| **Part 0** | `infra-foundation` — Monorepo、Docker (CPU/GPU)、Tunnel 與 CI | **P2 (底座)** | 一鍵啟動、NVIDIA GPU 支援、Cloudflare Tunnel HTTPS、S3/MinIO、CI | #1 | **已定案開單** | [#1](https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1) |

---

## 各部件範圍與 `/grill-me` 詢問清單

### Part 0 — `infra-foundation`（狀態：已開單可實作 — [Issue #1](https://github.com/qazwsx08ghj/DeepImageSearch_with_django/issues/1)）
- 完整規格書見 [`docs/specs/part-0-infra-foundation.md`](./specs/part-0-infra-foundation.md)。

### Part 1 — `vision-inference`（P0）
- **範圍：** 獨立 FastAPI (ASGI) 推論服務、單例載入 ONNX SigLIP/OpenCLIP、手寫 SLA-Aware Dynamic Micro-Batcher（`max_batch_size`、`max_wait_ms`、過期丟棄）、壓測用 Mock 模式。
- **`/grill-me` 必問清單：**
  1. 視覺模型選型（SigLIP-Base vs OpenCLIP ViT-B/32 vs MobileCLIP）與是否同步支援文字編碼（圖+文混合搜尋）？
  2. Dynamic Micro-Batcher 參數策略（`max_batch_size`、`max_wait_ms`、Queue 上限與 Load Shedding 回應碼）？
  3. 內部通訊協議（HTTP/2 vs gRPC）與 GPU Execution Provider（CUDA/TensorRT vs CPU fallback）？

### Part 2 — `vector-retrieval`（P0）
- **範圍：** PostgreSQL 16 + `pgvector` (0.8+) 版本化向量表（`model_version`）、兩階段檢索（量化粗排 ＋ 精排）、結合庫存與價格的 Iterative Scan 預過濾、Redis 兩層快取（圖片 SHA-256 與 `search_id` 篩選快取）。
- **`/grill-me` 必問清單：**
  1. 精度策略（`bit` Binary 粗排 ＋ `halfvec` 精排 vs 純 `halfvec`）？
  2. 同商品多張角度圖的去重與分數聚合方式（Max vs Weighted Avg）？
  3. 圖+文複合檢索權重與 `Exact Match` vs `Visually Similar` 分數門檻？

### Part 3 — `stream-gateway` & `mobile-edge`（P0）
- **範圍：** FastAPI WebSocket 串流層（Size-1 Latest-Frame-Wins Mailbox、`seq_id` 防亂序、閉環動態 `throttle`）＋ 手機優先 PWA 相機前端（`playsInline` 後鏡頭、`64×64` 穩定/模糊閘門、~30KB JPEG、1-in-flight 節流、條碼快路徑、底部抽屜購物卡）。
- **`/grill-me` 必問清單：**
  1. 前端技術棧（原生輕量 JS/Vite vs React/Vue vs Next.js）？
  2. 掃描互動模式（自動關鍵幀 ＋ 手動快門凍結並存）？
  3. 客戶端條碼快路徑與 Tier 2 瀏覽器輕量偵測器是否納入 v1？
  4. Server 下發 `throttle` 降頻的觸發指標（排隊深度 / P95 延遲 / GPU 使用率）？

### Part 4 — `commerce-core`（P1）
- **範圍：** Django 5 + DRF 商品目錄（多圖/變體/庫存）、購物車、原子扣庫存防超賣、`Idempotency-Key` 冪等結帳、未付款預留釋放、掃描轉化追蹤。
- **`/grill-me` 必問清單：**
  1. 單層 `Product` 還是含規格的 `Product + SKU Variant`？
  2. 下單直接扣庫存，還是「預扣 TTL ＋ 模擬付款 Webhook 確認／超時釋放」？
  3. 匿名訪客購物車（掃碼即買）＋ 選配 JWT 會員？
  4. 示範商品資料集選型（多品類零售樣本）？

### Part 5 — `async-indexer`（P1）
- **範圍：** 共用 Django ORM 的獨立建索引 Worker、可抽換 `EventBroker` 介面（預設 Redis Streams，可切換 RocketMQ/Kafka）、`realtime`/`bulk` 雙通道隔離、DB `BatchJob` + `lease_until` 斷點續傳、防亂序 `image_hash` 寫入與 DLQ 重放。
- **`/grill-me` 必問清單：**
  1. 批量匯入入口（CLI 管理指令 / CSV API / Django Admin）？
  2. Lease 逾時、最大重試次數與 DLQ 重放流程？
  3. 完整 Transactional Outbox Table 還是 `transaction.on_commit` ＋ 補償掃描？

### Part 6 — `observability-benchmarks`（P1）
- **範圍：** Prometheus + Grafana 儀表板（P50/P95/P99、Batch Size 直方圖、丟幀率、快取命中率、Stream Lag）＋ Locust/k6 壓測腳本驗證 5 大高併發與故障場景。
- **`/grill-me` 必問清單：**
  1. 壓測向量庫規模（例如本地 10 萬筆合成向量）與目標併發數？
  2. 壓測工具偏好（Locust vs k6）？
  3. 面試現場最想 Demo 哪 3 個高併發／故障對比實驗？
