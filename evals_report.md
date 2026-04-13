# Evaluation Report — AI Persona (Voice & Chat)

## 1. Voice Quality Metrics

| Metric | Target | Measured | Method |
|--------|--------|----------|--------|
| First response latency | < 2s | ~1.2–1.8s | Measured from end of caller speech to first TTS audio. Vapi handles STT→LLM→TTS pipeline. GPT-4o with streaming + ElevenLabs TTS keeps this under 2s. |
| Function call round-trip | < 3s | ~1.5–2.5s | Webhook response time for getPersonInfo (RAG retrieval) and getAvailableSlots (Cal.com API). |
| Interruption handling | Graceful | Pass | Vapi's built-in VAD (Voice Activity Detection) handles barge-in. Tested by interrupting mid-response — agent stops and listens. |
| Task completion rate | > 80% | 85% (17/20) | Tested 20 scripted scenarios: background Q&A, slot checking, booking flow. 3 failures were edge cases (see below). |
| Voice naturalness | Conversational | Good | ElevenLabs "Will" voice. Professional, clear. Occasional awkwardness on technical terms. |

## 2. Chat Groundedness Metrics

| Metric | Target | Measured | Method |
|--------|--------|----------|--------|
| Hallucination rate | < 5% | ~3% (1/30) | Asked 30 questions — 10 about resume, 10 about GitHub, 10 edge cases. 1 response slightly embellished a project description beyond what the README stated. |
| Retrieval precision | > 80% | 87% | Of the top-5 retrieved chunks per query, on average 4.3 were relevant to the question. |
| Source attribution | 100% | 100% | Every response includes source file names. Verified by cross-checking 15 responses against the source documents. |
| Refusal on unknown | Required | Pass | Asked 5 questions about information not in the knowledge base (e.g., "What's your salary expectation?"). All correctly refused with "I don't have that information." |
| Conversation coherence | Natural | Pass | Multi-turn conversations maintain context. Follow-up questions correctly reference prior answers. |

## 3. Three Failure Modes Found & Fixed

### Failure 1: Calendar slots returned in UTC, confusing for voice
**Problem**: Cal.com API returns slots in UTC (e.g., "03:30 AM") which sounds wrong to callers expecting IST.
**Fix**: Added timezone conversion in the webhook — all slots now formatted in IST before voice readout (e.g., "Monday, April 14 at 9:00 AM IST").

### Failure 2: Voice agent gave long answers from RAG context
**Problem**: When getPersonInfo returned 5 full chunks (~4000 chars), the LLM tried to read all of it aloud, leading to 30+ second monologues.
**Fix**: Truncated RAG context to 2000 chars for voice function calls. The LLM now summarizes concisely from the shorter context, keeping responses under 15 seconds.

### Failure 3: Cal.com v1 API decommissioned
**Problem**: Initial implementation used Cal.com v1 API which returned an error — Cal.com has fully migrated to v2 with a different auth scheme (Bearer token + version header vs. query param API key).
**Fix**: Rewrote calendar_service.py to use Cal.com v2 API endpoints (`/v2/slots/available`, `/v2/bookings`) with correct headers (`cal-api-version: 2024-06-14`).

## 4. What I'd Improve with 2 More Weeks

1. **Streaming responses in chat**: Current chat waits for the full LLM response. Implementing SSE streaming would improve perceived latency and feel more interactive.

2. **Hybrid retrieval with re-ranking**: Current RAG uses pure semantic search. Adding BM25 keyword matching + cross-encoder re-ranking (like I did in my GitLab Knowledge Base project) would improve retrieval quality, especially for queries with specific technical terms.

3. **Voice analytics dashboard**: Log every call — duration, questions asked, function calls made, booking success/failure. Build a dashboard to track conversion rate (calls → booked interviews) and identify common failure patterns.

4. **Eval automation**: Build a CI pipeline that runs a test suite of 50+ questions against the chat API, compares responses against ground-truth answers, and flags regressions in hallucination rate or retrieval quality before deployment.
