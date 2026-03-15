# 🔀 Multi-LLM Router

A FastAPI application that routes prompts to multiple LLM providers simultaneously — **Claude (Anthropic)**, **GPT-3.5 (OpenAI)**, and **LLaMA3 (Groq)** — and returns a cost + latency comparison so you can pick the best model for your use case.

Built by **Harwinder Singh** — Operations Architect & AI Automation Engineer

---

## 🚀 Live Demo
Deployed on Render — [coming soon]

---

## 🧠 What It Does

Send one prompt → get responses from 3 LLMs simultaneously → see which is fastest, cheapest, and recommended.

---

## 🏗️ Architecture
```
User Request (prompt)
        │
        ▼
  FastAPI /route
        │
   ┌────┴────┐
   │ asyncio │  (parallel calls)
   └────┬────┘
        │
┌───────┼───────┐
▼       ▼       ▼
Groq  OpenAI  Anthropic
        │
        ▼
  Compare Results
  (latency + cost)
        │
        ▼
  Return Winner
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-purple)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Render](https://img.shields.io/badge/Deployed-Render-brightgreen)

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/harwinder-singh-dev/multi-llm-router.git
cd multi-llm-router
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Open API docs
```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Server status |
| POST | `/route` | Route prompt to all LLMs |

---

## 📨 Example Request
```json
POST /route
{
  "prompt": "Explain what an API is in one sentence.",
  "max_tokens": 100
}
```

## ✅ Example Response
```json
{
  "prompt": "Explain what an API is in one sentence.",
  "fastest_model": "llama3-8b-8192",
  "cheapest_model": "llama3-8b-8192",
  "recommended_model": "llama3-8b-8192",
  "results": [
    {
      "model": "llama3-8b-8192",
      "provider": "Groq",
      "response": "An API is a set of rules...",
      "latency_seconds": 0.43,
      "estimated_cost_usd": 0.000012
    }
  ]
}
```

---

## 💰 Cost Comparison Table

| Provider | Model | Cost per 1K tokens |
|----------|-------|-------------------|
| Groq | LLaMA3-8B | $0.0001 |
| Groq | LLaMA3-70B | $0.0008 |
| OpenAI | GPT-3.5 Turbo | $0.0015 |
| Anthropic | Claude Haiku | $0.00025 |

---

## 🐳 Docker
```bash
docker build -t multi-llm-router .
docker run -p 8000:8000 --env-file .env multi-llm-router
```

---

## 📁 Project Structure
```
multi-llm-router/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app & endpoints
│   ├── router.py      # LLM provider calls
│   └── models.py      # Request/response schemas
├── .env.example       # Environment variables template
├── requirements.txt   # Dependencies
├── Dockerfile         # Container setup
└── README.md
```

---

## 👤 Author

**Harwinder Singh**
Operations Architect • Automation Engineer • AI Systems
📍 Hoshiarpur, Punjab, India
🔗 [LinkedIn](https://linkedin.com/in/harwinder-singh-16a6572a6)
📧 harwindersingh2482@gmail.com