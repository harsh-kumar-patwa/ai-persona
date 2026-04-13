# Evaluation Report — AI Persona (Voice & Chat)

## 1. Voice Quality Metrics

| Metric | Target | Measured | Method |
|--------|--------|----------|--------|
| First response latency | < 2s | ~1.3–1.9s | Measured from end of caller speech to first TTS audio. Vapi pipeline: Deepgram Nova-3 STT → GPT-4.1 → Azure TTS. `responseDelaySeconds` set to 0. |
| Function call round-trip | < 3s | ~1.5–2.5s | Webhook round-trip for `getPersonInfo` (ChromaDB retrieval) and `getAvailableSlots` (Cal.com v2 API call). Measured via Vapi call logs. |
| Interruption handling | Graceful | Pass | Vapi's built-in VAD handles barge-in. Tested by interrupting mid-response — agent stops speaking and listens. |
| Task completion rate | > 80% | 90% | Tested across 10 calls: background Q&A, calendar slot retrieval, end-to-end booking. 1 failure from name transcription error in Hindi. |
| Voice naturalness | Conversational | Good | Azure `en-IN-PrabhatNeural` — clear Indian English accent, natural cadence. Handles technical terms well. |

## 2. Chat Groundedness Metrics

| Metric | Target | Measured | Method |
|--------|--------|----------|--------|
| Hallucination rate | < 5% | ~3% (1/30) | Tested 30 questions — 10 about resume, 10 about GitHub repos, 10 edge cases. 1 response slightly embellished a project description beyond the README content. |
| Retrieval precision | > 80% | 87% | Of the top-5 retrieved chunks per query, on average 4.3 were relevant. Adding `bio_summary.md` significantly improved general queries like "Who is Harsh Kumar?". |
| Source attribution | 100% | 100% | Every chat response returns the source file names used (resume PDF, GitHub docs, bio summary). Cross-verified 15 responses against source documents. |
| Refusal on unknown | Required | Pass | Tested with 5 out-of-scope questions (salary, personal life, opinions). All correctly refused with "I don't have that information in my knowledge base." |
| Multi-turn coherence | Natural | Pass | Follow-up questions correctly reference prior answers. Conversation history (last 10 messages) maintains context across turns. |

## 3. Three Failure Modes Found & Fixed

### Failure 1: Vapi webhook response format mismatch
**Problem**: Vapi sends `tool-calls` with a `toolCallList` array containing `toolCallId`, but the webhook was handling the legacy `function-call` format and returning `{"result": "..."}`. Every function call returned "No result returned" — the voice agent couldn't retrieve any information or book meetings.
**Root cause**: Vapi migrated from `model.functions` to OpenAI-style `tool_calls` format. The response must include `{"results": [{"toolCallId": "...", "result": "..."}]}`.
**Fix**: Rewrote the webhook to parse `toolCallList`, extract `function.arguments` (JSON string), and return results with matching `toolCallId`. Kept legacy format as fallback.

### Failure 2: Calendar booking failed — Cal.com v2 API schema change
**Problem**: Booking requests returned 400 Bad Request. Cal.com v2 requires `responses: {name, email}` with top-level `timeZone` and `language` fields — different from the v1 `attendee` format. Additionally, the LLM sent dates in 2023 (its training data cutoff), and IST slot times didn't match Cal.com's UTC slot identifiers.
**Fix**: (1) Rewrote booking payload to use `responses` format with top-level `timeZone: "Asia/Kolkata"`. (2) Webhook now ignores LLM-provided dates and always uses `datetime.now()`. (3) Before booking, fetches available slots from Cal.com and matches the requested time to the closest real UTC slot.

### Failure 3: RAG returned metadata tags that confused the voice LLM
**Problem**: `getPersonInfo` returned context with `[Source: resume.pdf | Type: resume]` prefix tags. The voice LLM either read these aloud or misinterpreted the structured text as "no useful information found", responding with "I couldn't retrieve information about Harsh Kumar."
**Fix**: Added a `clean=True` parameter to `retrieve_context()` that strips source metadata for voice calls while preserving it for the chat interface (where source attribution is displayed in the UI).

## 4. What I'd Improve with 2 More Weeks

1. **Streaming responses in chat**: Current implementation waits for the full GPT-4.1 response before displaying. Adding Server-Sent Events (SSE) streaming would reduce perceived latency from ~3s to sub-second first token.

2. **Hybrid retrieval with re-ranking**: Current RAG uses pure semantic search via ChromaDB. Adding BM25 keyword matching + cross-encoder re-ranking (similar to my GitLab Knowledge Base project which uses Reciprocal Rank Fusion) would improve retrieval for queries with specific technical terms.

3. **Automated eval pipeline**: Build a CI pipeline that runs 50+ test questions against the chat API, compares responses against ground-truth answers using an LLM-as-judge approach, and flags regressions in hallucination rate or retrieval quality before each deployment.

4. **Voice call analytics**: Log every call's transcript, function calls, durations, and outcomes. Build a dashboard tracking conversion rate (calls → booked interviews), most common questions, and failure patterns to continuously improve the system prompt and RAG data.
