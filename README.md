# Persian RAG Starter 🇮🇷

A production-ready RAG (Retrieval Augmented Generation) starter kit optimized for Persian language.

## Features

- **Persian-aware chunking** — splits on sentence boundaries, not character count
- **Auto language detection** — picks the right embedding model for Persian or English
- **Streaming responses** — real-time token-by-token output
- **Authentication** — API key protection
- **Caching** — avoid duplicate API calls
- **Rate limiting** — protect against abuse
- **Monitoring** — request logging with duration
- **Docker ready** — one command deploy

## Stack

```
FastAPI + ChromaDB + Ollama + sentence-transformers
```

## Quick Start

```bash
git clone https://github.com/hosivay/persian-rag-starter
cd persian-rag-starter
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## API

```bash
# Add document
curl -X POST http://localhost:8000/add \
  -H "x-api-key: dev-key-123" \
  -d '{"text": "متن شما", "doc_id": "doc_1"}'

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "x-api-key: dev-key-123" \
  -d '{"query": "سوال شما"}'
```

## Examples

```bash
python examples/shiraz_guide.py
```

## Tests

```bash
pytest tests/ -v
```

---

# Persian RAG Starter 🇮🇷

یک استارتر کیت آماده برای ساخت سیستم RAG بهینه‌شده برای زبان فارسی.

## ویژگی‌ها

- **تقسیم‌بندی هوشمند فارسی** — بر اساس جمله، نه تعداد کاراکتر
- **تشخیص خودکار زبان** — انتخاب مدل مناسب برای فارسی یا انگلیسی
- **پاسخ استریمینگ** — خروجی توکن به توکن
- **احراز هویت** — محافظت با API Key
- **کشینگ** — جلوگیری از درخواست‌های تکراری
- **محدودیت نرخ** — محافظت در برابر سوءاستفاده
- **مانیتورینگ** — لاگ درخواست‌ها با زمان پاسخ
- **Docker** — دیپلوی با یک دستور

## نصب سریع

```bash
git clone https://github.com/hosivay/persian-rag-starter
cd persian-rag-starter
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```