# AI Persona — Voice & Chat Agent

An AI-powered personal representative that can answer questions about my background, skills, and projects via **phone call** or **web chat**, and book interviews on my real calendar — fully autonomous, no human in the loop.

Built for the Scaler Screening Assignment.

## Live Links

| Channel | Link |
|---------|------|
| **Voice Agent** | Call **+1 (858) 251-5006** |
| **Chat Interface** | [harsh-ai-assistant.harshkumarpatwa.in](https://harsh-ai-assistant.harshkumarpatwa.in) |
| **Book Interview** | [cal.com/harsh-kumar-lodmok/15min](https://cal.com/harsh-kumar-lodmok/15min) |

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                              USER                                    │
│                    (Phone Call / Web Chat)                            │
└──────────┬───────────────────────────────┬───────────────────────────┘
           │                               │
           ▼                               ▼
┌─────────────────────┐         ┌─────────────────────────┐
│   Vapi Voice Agent   │         │   Next.js 16 Frontend    │
│                      │         │                          │
│  • Azure TTS         │         │  • TypeScript            │
│    (en-IN-Prabhat)   │         │  • Tailwind CSS          │
│  • Deepgram STT      │         │  • Session management    │
│  • GPT-4.1           │         │  • Suggested prompts     │
│  • Phone: +1 858     │         │  • Booking link          │
└──────────┬───────────┘         └────────────┬─────────────┘
           │                                  │
           │  Function Calls (HTTPS)          │  REST API
           ▼                                  ▼
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Backend                         │
│                                                           │
│   ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  │
│   │  /api/chat   │  │  /api/vapi    │  │ /api/calendar │  │
│   │              │  │  /webhook     │  │ /slots /book  │  │
│   └──────┬───────┘  └──────┬────────┘  └──────┬────────┘  │
│          │                 │                   │           │
│          ▼                 ▼                   ▼           │
│   ┌────────────────────────────┐     ┌─────────────────┐  │
│   │      RAG Service           │     │ Calendar Service │  │
│   │                            │     │                  │  │
│   │  Query → Embed → Retrieve  │     │  Cal.com v2 API  │  │
│   │  → Context → GPT-4.1      │     │  Real booking    │  │
│   │  → Grounded Response       │     │  IST timezone    │  │
│   └────────────┬───────────────┘     └──────────────────┘  │
│                │                                           │
│                ▼                                           │
│   ┌────────────────────────────┐                           │
│   │    ChromaDB Vector Store   │                           │
│   │                            │                           │
│   │  • Resume PDF chunks       │                           │
│   │  • GitHub repo docs        │                           │
│   │  • Bio summary             │                           │
│   │  • text-embedding-3-small  │                           │
│   └────────────────────────────┘                           │
└──────────────────────────────────────────────────────────────┘

Infrastructure: EC2 (t3.small) → Docker Compose → Nginx (SSL) → Let's Encrypt
Images hosted on AWS ECR (ap-south-1)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Voice Agent** | Vapi + Azure TTS (en-IN-PrabhatNeural) + Deepgram Nova-3 STT + GPT-4.1 |
| **Chat Frontend** | Next.js 16, TypeScript, Tailwind CSS |
| **Backend API** | FastAPI (Python) |
| **RAG Pipeline** | LangChain + OpenAI Embeddings (`text-embedding-3-small`) + ChromaDB |
| **LLM** | GPT-4.1 (temperature 0.3) |
| **Calendar** | Cal.com v2 API (real availability, real bookings) |
| **Infrastructure** | AWS EC2, ECR, Docker Compose, Nginx, Let's Encrypt SSL |
| **Telephony** | Vapi managed phone number (+1 858) |

## Project Structure

```
scaler/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app, CORS, lifespan
│   │   ├── config.py                # Environment config
│   │   ├── routers/
│   │   │   ├── chat.py              # POST /api/chat/
│   │   │   ├── calendar.py          # GET /api/calendar/slots, POST /api/calendar/book
│   │   │   └── vapi_webhook.py      # POST /api/vapi/webhook (Vapi function calls)
│   │   ├── services/
│   │   │   ├── rag_service.py       # ChromaDB vector store, retrieval, LLM chat
│   │   │   ├── calendar_service.py  # Cal.com v2 integration (slots + booking)
│   │   │   └── github_service.py    # GitHub API — fetch repos + READMEs
│   │   └── data/                    # Resume PDF + GitHub docs + bio summary
│   ├── scripts/
│   │   ├── ingest_github.py         # Fetch GitHub repos → markdown for RAG
│   │   └── setup_vapi.py            # Create Vapi assistant + phone number
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx           # Root layout with metadata
│   │   │   ├── page.tsx             # Main page with header + booking link
│   │   │   └── globals.css          # Tailwind + custom styles
│   │   └── components/
│   │       └── Chat.tsx             # Chat UI — messages, input, suggested questions
│   ├── Dockerfile
│   ├── next.config.ts               # standalone output for Docker
│   └── package.json
├── deploy/
│   └── setup-ec2.sh                 # EC2 bootstrap script
├── docker-compose.yml               # Backend + Frontend + Nginx
├── nginx.conf                       # Reverse proxy with SSL
├── evals_report.md                  # Evaluation report
└── README.md
```

## How It Works

### RAG Pipeline
Resume PDF, GitHub repo data, and a bio summary are chunked using `RecursiveCharacterTextSplitter` (800 chars, 200 overlap), embedded with `text-embedding-3-small`, and stored in ChromaDB. On each query, the top-5 most relevant chunks are retrieved and passed as context to GPT-4.1 with a system prompt that enforces grounded responses.

### Chat Interface
Next.js frontend sends messages to the FastAPI `/api/chat` endpoint. The backend retrieves relevant context from ChromaDB, builds a prompt with conversation history (last 10 messages), and returns a grounded response with source attribution. The UI shows source files used for each answer.

### Voice Agent
Vapi handles telephony (phone number), STT (Deepgram Nova-3), and TTS (Azure en-IN-PrabhatNeural). When the LLM needs factual information, it calls `getPersonInfo` which triggers a webhook to our backend for RAG retrieval. Calendar operations (`getAvailableSlots`, `bookMeeting`) go through the same webhook to the Cal.com v2 API. The webhook always uses real-time dates and converts slots to IST.

### Calendar Booking
Real Cal.com v2 integration with live availability. Both voice and chat can trigger bookings that create actual calendar events with email confirmations. The webhook automatically matches requested times to the closest available Cal.com slot in UTC.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (for deployment)
- API keys: OpenAI, Vapi, Cal.com

### 1. Backend (Local Dev)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your API keys in .env

# Ingest GitHub data
python scripts/ingest_github.py

# Place your resume PDF in backend/app/data/

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Frontend (Local Dev)

```bash
cd frontend
npm install
# Create .env.local with:
#   NEXT_PUBLIC_API_URL=http://localhost:8001
#   NEXT_PUBLIC_CALCOM_LINK=https://cal.com/your-username/15min
npm run dev
```

### 3. Voice Agent Setup

```bash
# Expose backend for Vapi webhook (local dev)
ngrok http 8001

# Create Vapi assistant + phone number
cd backend && source venv/bin/activate
python scripts/setup_vapi.py <ngrok-https-url> "Your Name"
```

### 4. Production Deployment (EC2 + ECR)

```bash
# Build and push images to ECR
docker buildx build --platform linux/amd64 -t ai-persona-backend --load ./backend
docker buildx build --platform linux/amd64 -t ai-persona-frontend --load ./frontend

# Tag and push to ECR
docker tag ai-persona-backend:latest <account>.dkr.ecr.<region>.amazonaws.com/ai-persona-backend:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/ai-persona-backend:latest

# On EC2: pull images + docker compose up
# See deploy/setup-ec2.sh for full bootstrap script

# SSL via certbot
sudo certbot certonly --standalone -d your-domain.com
```

## Key Design Decisions

1. **ChromaDB over Pinecone/Weaviate** — No external vector DB dependency. Runs in-process, good enough for ~30 document chunks. Simplifies deployment.

2. **Webhook-side date handling** — The LLM doesn't know the current date, so the webhook ignores whatever dates GPT sends and always uses `datetime.now()` for calendar queries. No hardcoded dates.

3. **Cal.com v2 slot matching** — When booking, the webhook fetches available slots from Cal.com and matches the requested time to the closest real slot. This prevents booking failures from timezone mismatches.

4. **Clean context for voice** — RAG retrieval strips source metadata tags before sending to the voice agent, preventing the LLM from reading "[Source: resume.pdf | Type: resume]" aloud.

5. **Azure TTS over ElevenLabs** — Switched to Azure `en-IN-PrabhatNeural` for a recognizable Indian English accent that handles both English and Hindi content naturally.
