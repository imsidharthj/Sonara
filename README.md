# Sonara — Voice AI E-Commerce Support Assistant

A production-quality voice support assistant for e-commerce returns and orders. Speak into your browser mic, get intelligent voice responses powered by AI.

```
Browser Mic → Groq Whisper STT → LangGraph Agent (GPT-4o-mini) → ElevenLabs TTS → Voice Response
```

## Setup

1. **Clone and install:**
```bash
git clone <repo-url> && cd Sonara
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API keys** — copy `.env.example` to `.env` and fill in:
```
GROQ_API_KEY=         # groq.com
OPENAI_API_KEY=       # platform.openai.com
ELEVENLABS_API_KEY=   # elevenlabs.io
ELEVENLABS_VOICE_ID=  # voice ID from ElevenLabs dashboard
```

3. **Run:**
```bash
uvicorn main:app --reload
```
Open http://localhost:8000 — tap the mic, ask about an order.

## Architecture

```
voice-support-assistant/
├── main.py                  # FastAPI entry point, /voice and /health endpoints
├── agent/
│   ├── graph.py             # LangGraph ReAct agent with session memory
│   ├── tools.py             # lookup_order, check_return_eligibility
│   └── prompts.py           # System prompt with policy injection
├── voice/
│   ├── stt.py               # Groq Whisper STT
│   └── tts.py               # ElevenLabs TTS → base64
├── data/
│   ├── orders.json          # Order dataset
│   ├── policies.json        # Policy dataset
│   └── data_store.py        # Loads JSON into memory at startup
└── static/
    └── index.html           # Single-page voice UI
```

**Pipeline flow:**
```
POST /voice (audio file + session_id)
  │
  ├─ Groq Whisper STT → transcript
  ├─ LangGraph Agent → reply (uses tools to query orders/policies)
  └─ ElevenLabs TTS → audio_base64
  │
  └─ Response: { transcript, reply_text, audio_base64, session_id }
```

## Assumptions

- **Static dataset:** Orders and policies are loaded from JSON files into memory at startup. No database, no vector store.
- **In-memory sessions:** Conversation history is stored per-session in a Python dict. Lost on server restart.
- **Single-user demo:** No authentication. Session isolation is by UUID only.
- **Browser-only:** Requires a modern browser with `MediaRecorder` API support.

## Design Decisions & Tradeoffs

| Decision | Rationale |
|----------|-----------|
| **LangGraph over LangChain** | Minimal ReAct agent with `create_react_agent` — 2 tools, no chain overhead. LangGraph gives explicit graph control without LangChain's abstraction layers. |
| **Groq for STT** | Ultra-low latency Whisper transcription via Groq's inference API. Free tier available. Beats self-hosted Whisper on speed. |
| **In-memory sessions over Redis** | Demo scale — no infrastructure dependency. Dict lookup is instant. At scale, swap for Redis or a session store. |
| **No vector DB** | Policy document is small enough to inject directly into the system prompt. Order lookup is by ID, not semantic search. A vector DB would add complexity with zero benefit here. |
| **Vanilla HTML/JS frontend** | Zero build step, zero dependencies. Ships as a single file. MediaRecorder API handles mic capture natively. |
| **Errors surface to user with retry** | No silent retries or fallback logic. If something fails, the user sees the error and can retry manually. |

## What I'd Do Differently at Scale

- **Persistent session store** (Redis/DynamoDB) for conversation history that survives restarts and scales horizontally
- **Async streaming TTS** — stream audio chunks back as they're generated instead of waiting for the full synthesis
- **Database with retrieval layer** — replace JSON files with PostgreSQL + optional vector search for large catalogs
- **User authentication** — JWT/OAuth to tie sessions to real user accounts and their specific order history
- **WebSocket connection** — replace request/response with a persistent socket for real-time voice streaming
- **Rate limiting and observability** — request throttling, latency tracking, error alerting
