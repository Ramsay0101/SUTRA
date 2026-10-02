# Sutra (सूत्र) — AI-Native Institutional Learning Operating System

> **"The Connecting Thread"** — An AI-native institutional operating system unifying epistemic knowledge tracing, 2-pass agentic grading, grounded epistemic RAG, and multi-agent coordination.

---

## 🏗️ Architecture Overview

Sutra is architected as a production-grade distributed system:
* **Single Source of Truth:** PostgreSQL 16 with kernel-level Row-Level Security (RLS) and Transactional Outbox for Change Data Capture (CDC).
* **Universal Identity & Dynamic Entity Spine:** Decoupled Universal User identity with 18-type metadata-driven dynamic collections and 2-mode capability suite grants.
* **Dual Graph Topology (Phase 1):** Neo4j Concept DAG and Institutional Social Topology for recursive prerequisite skill repair.
* **Epistemic Hybrid RAG (Phase 2):** Dense vector + Sparse BM25 retrieval with Reciprocal Rank Fusion ($RRF$) and physical bounding-box citations.
* **Agentic Grading Core (Phase 3):** 2-Pass deterministic rubrics, Tree-sitter AST anti-plagiarism hashing, and isolated code execution sandboxes.
* **Continuous BKT Engine (Phase 4):** Continuous Bayesian Knowledge Tracing ($C\text{-}BKT$) with soft-evidence likelihood weighting.
* **FastMCP Swarm (Phase 5):** 3-Tier governed tool execution (`Read`, `Notify`, `Propose-and-Approve`) with AST query sandboxing (`sqlglot`).
* **Edge Privacy Proxy (Phase 6):** Local CPU Presidio/GLiNER ONNX PII tokenization and WebAssembly proctoring.

---

## 📁 Repository Structure

```
.
├── backend/                  # FastAPI & SQLAlchemy 2.0 Async Core
│   ├── alembic/              # Database schema migrations
│   ├── src/
│   │   ├── core/             # Centralized settings & Pydantic config
│   │   ├── domain/           # Pure domain models, enums, & business logic
│   │   └── infrastructure/   # Database session, models, repositories
│   ├── tests/                # Async test suite
│   └── pyproject.toml        # Python project dependencies
├── .gitignore                # Production ignore rules
└── README.md
```

---

## 🚀 Getting Started (Backend)

### 1. Prerequisites
* Python 3.12+
* PostgreSQL 16+
* Redis 7+

### 2. Setup Virtual Environment
```bash
cd backend
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sutra
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key-change-in-production
ENVIRONMENT=development
DEBUG=True
```

---

## 📜 License
Proprietary / All Rights Reserved.
