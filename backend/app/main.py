from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.services.rag_service import init_vectorstore
from app.routers import chat, calendar, vapi_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize vector store
    print("Initializing vector store...")
    init_vectorstore()
    print("Vector store ready.")
    yield
    # Shutdown
    print("Shutting down.")


app = FastAPI(
    title="AI Persona API",
    description="RAG-powered AI persona for Scaler screening assignment",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(calendar.router)
app.include_router(vapi_webhook.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Persona API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
