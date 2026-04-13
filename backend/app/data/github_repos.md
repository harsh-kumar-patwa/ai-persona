# GitHub Profile: harsh-kumar-patwa

## Repository: gitlab-knowledge-base
URL: https://github.com/harsh-kumar-patwa/gitlab-knowledge-base
Description: AI-powered chatbot for GitLab Handbook
Primary Language: Python
Tech Stack: FastAPI, Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui, PostgreSQL, ChromaDB, Google Gemini 2.5 Flash, Gemini Embeddings, Cross-encoder re-ranking, Docker, Railway, Vercel
Purpose: RAG application that scrapes, indexes, and retrieves information from GitLab's public handbook and direction pages through a conversational interface.
Key Features:
- Hybrid Search: Semantic embeddings + BM25 keyword matching + cross-encoder re-ranking with Reciprocal Rank Fusion
- Streaming Responses with source citations
- Guardrails: Off-topic detection, relevance scoring, hallucination prevention
- Analytics Dashboard for query tracking
- Batch Embedding Pipeline for optimized ingestion
- Live Sync to refresh data from GitLab
Tradeoffs: Chose hybrid retrieval (semantic + BM25 + RRF) over pure semantic search for better accuracy. Used cross-encoder re-ranking which adds latency but significantly improves result quality. PostgreSQL for structured data + ChromaDB for vectors rather than a single vector-native DB.

## Repository: Blood-Test-Report-Analyser
URL: https://github.com/harsh-kumar-patwa/Blood-Test-Report-Analyser
Description: AI-powered blood test report analysis
Primary Language: Python
Tech Stack: FastAPI, Streamlit, Gemini AI, Multi-agent architecture
Purpose: Analyzes blood test reports using AI agents, searches for relevant health articles, and generates personalized health recommendations.
Architecture: Multi-agent system with separate Analysis Agent, Recommendation Agent, and Search Agent, each extending a base agent class.
Key Features:
- PDF parsing for blood test reports
- Multi-agent AI system for analysis and recommendations
- Web search integration for health articles
- CLI and Web UI versions
Tradeoffs: Used multi-agent architecture for separation of concerns. Chose Streamlit for rapid UI prototyping over a full React frontend.

## Repository: verifAI
URL: https://github.com/harsh-kumar-patwa/verifAI
Primary Language: Python
Purpose: AI verification tool

## Repository: identity-reconciliation-service
URL: https://github.com/harsh-kumar-patwa/identity-reconciliation-service
Description: Customer identity reconciliation API - Links contacts across multiple purchases
Primary Language: TypeScript
Tech Stack: Node.js, TypeScript, Express 5, Prisma 7, SQLite
Purpose: Web service that links customer contacts across multiple purchases using email and phone number. Implements Bitespeed backend identity reconciliation.
Key Features:
- POST /identify endpoint for contact linking
- Automatic primary/secondary contact management
- If request links two separate primaries, older one stays primary
Tradeoffs: Used SQLite for simplicity and portability. Prisma ORM for type-safe database queries. Express 5 for modern async error handling.

## Repository: chatbot-flow-builder
URL: https://github.com/harsh-kumar-patwa/chatbot-flow-builder
Primary Language: TypeScript
Tech Stack: React, TypeScript, Vite
Purpose: Visual chatbot flow builder with drag-and-drop interface

## Repository: SyncStream
URL: https://github.com/harsh-kumar-patwa/SyncStream
Description: Two-way Stripe integration with Kafka
Primary Language: Python
Tech Stack: Python, Docker, Docker Compose, Kafka, Stripe API, Ngrok
Purpose: Two-way integration between a local customer catalog and Stripe with near real-time synchronization using Kafka as a message queue.
Key Features:
- Bidirectional sync between local DB and Stripe
- Kafka message queue for reliable event processing
- Stripe webhook integration via Ngrok
- Docker Compose for full infrastructure
Tradeoffs: Kafka for message queue ensures reliability and ordering. Docker Compose for easy local development. Ngrok for webhook development without deploying.

## Repository: youtube-video-fetcher
URL: https://github.com/harsh-kumar-patwa/youtube-video-fetcher
Description: Go-based YouTube video fetcher API
Primary Language: Go
Tech Stack: Go, SQLite3, YouTube Data API v3
Purpose: API that fetches latest videos from YouTube based on search queries, stores them in a database, and provides a web interface to view and interact with stored videos.
Key Features:
- Background worker for continuous video fetching
- Web interface for browsing fetched videos
- Configurable search queries and API key rotation
Tradeoffs: Go for performance and concurrency. SQLite for embedded simplicity. Multiple API key support for rate limit handling.

## Repository: DSA_Helper
URL: https://github.com/harsh-kumar-patwa/DSA_Helper
Description: DSA Learning Assistant with AI chat
Primary Language: Python
Tech Stack: Python, Streamlit, Gemini AI, Graph algorithms
Deployed: https://harshkumarpatwa-dsa.streamlit.app/
Purpose: Web application that helps users identify optimal learning paths for DSA topics using graph algorithms (topological sorting) and provides AI-powered chat assistance.
Key Features:
- Topic dependency analysis using topological sorting
- AI Chat Assistant powered by Gemini
- Curated practice problems by difficulty
- Graph-based prerequisite resolution
Tradeoffs: Used graph algorithms for topic ordering rather than a static list. Streamlit for rapid deployment. Gemini for cost-effective AI responses.

## Repository: logo-detection
URL: https://github.com/harsh-kumar-patwa/logo-detection
Description: Pepsi and CocaCola logo detection in video
Primary Language: Python
Tech Stack: Python, YOLOv9, OpenCV, Roboflow
Purpose: ML pipeline to detect Pepsi and CocaCola logos in video files. Extracts frames, detects logos, returns timestamps as JSON.
Tradeoffs: YOLOv9 for state-of-the-art detection speed and accuracy. Roboflow for dataset management and augmentation.

## Repository: Person-PPE-Detection
URL: https://github.com/harsh-kumar-patwa/Person-PPE-Detection
Description: Two-stage PPE detection system
Primary Language: Python
Tech Stack: Python, YOLO (Ultralytics), OpenCV
Purpose: Two-stage detection system for Personal Protective Equipment in workplace environments. First detects persons, then identifies PPE items worn by each person.
Architecture: Two-stage pipeline — person detection model followed by PPE detection model on cropped regions.
Tradeoffs: Two-stage approach allows separate optimization of person detection and PPE classification. More accurate than single-stage for this use case.

## Repository: study_assistant
URL: https://github.com/harsh-kumar-patwa/study_assistant
Description: Intelligent query routing study assistant
Primary Language: Python
Tech Stack: Python, Gemini AI, RAG
Purpose: Intelligent query routing system using RAG to assist students. Classifies queries by subject, retrieves from subject-specific transcripts, generates responses with source attribution.
Key Features:
- Query classification into subjects or general knowledge
- Subject-specific document retrieval
- Clear source indication (retrieved vs. general knowledge)

## Repository: parking-lot-LLD
URL: https://github.com/harsh-kumar-patwa/parking-lot-LLD
Primary Language: Java
Purpose: Low-level design implementation of a parking lot system with UML diagrams

## Repository: devops-assignment
URL: https://github.com/harsh-kumar-patwa/devops-assignment
Primary Language: Java
Purpose: DevOps assignment implementation

## Repository: Devops-Notes
URL: https://github.com/harsh-kumar-patwa/Devops-Notes
Purpose: DevOps learning notes and documentation

## Repository: atm-lld
URL: https://github.com/harsh-kumar-patwa/atm-lld
Purpose: Low-level design of an ATM system

## Repository: snake-ladder-LLD
URL: https://github.com/harsh-kumar-patwa/snake-ladder-LLD
Purpose: Low-level design of Snake and Ladder game

## Repository: register-login-auth
URL: https://github.com/harsh-kumar-patwa/register-login-auth
Primary Language: JavaScript
Purpose: Authentication system with registration and login

## Repository: chatbot-bot9
URL: https://github.com/harsh-kumar-patwa/chatbot-bot9
Primary Language: JavaScript
Purpose: Chatbot implementation

## Repository: chatbot-frontend
URL: https://github.com/harsh-kumar-patwa/chatbot-frontend
Primary Language: JavaScript
Purpose: Frontend for chatbot application
