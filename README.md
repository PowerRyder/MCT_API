# MCT_API – Multi-Channel Trading Platform (Backend)

**MCT_API** is the backend REST API for the **Multi-Channel Trading (MCT)** platform. Built using **FastAPI**, it handles user authentication, trade execution, exchange integrations, balance tracking, and signal processing across multiple cryptocurrency exchanges.

---

## 🚀 Features

- 🔐 JWT-based Authentication System
- 🧾 User Management (Register/Login/Profile)
- 🔄 Multi-Exchange Support (Binance, KuCoin, etc.)
- 📈 Trade Execution (Buy/Sell via API)
- 💼 Real-Time Balance & Open Orders
- 💬 Strategy Signal Ingestion via Webhooks
- 🧠 Modular Design for Strategy Plugins

---

## 🛠️ Tech Stack

- **FastAPI** – Web API framework
- **PostgreSQL** – Relational database
- **SQLAlchemy / Tortoise ORM** – Database models
- **Uvicorn** – ASGI server
- **Pydantic** – Request/response schema validation
- **CCXT** – Unified crypto exchange trading library
- **PassLib / JWT** – Authentication & password security

---
