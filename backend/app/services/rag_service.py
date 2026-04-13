import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document, HumanMessage, SystemMessage
from app.config import OPENAI_API_KEY, CHROMA_PERSIST_DIR, DATA_DIR

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4.1", temperature=0.3)

vectorstore = None
# session_id -> list of {"role": "user"|"assistant", "content": str}
session_histories: dict[str, list[dict]] = {}

SYSTEM_PROMPT = """You are an AI persona representing the person whose resume and GitHub profile you have access to.
You speak in first person as their AI representative.

Your role:
- Answer questions about their background, skills, experience, and projects accurately
- Be specific and cite real details from the provided context
- If asked about something not in your knowledge base, say "I don't have specific information about that in my knowledge base" — never make things up
- Be conversational, confident, and professional
- When asked about GitHub repos, explain the tech stack, purpose, and design tradeoffs
- When asked why they're right for a role, give specific, compelling evidence from their actual experience
- When the user wants to schedule an interview or book a call, tell them they can use the "Book Interview" button at the top of the page, which links to the Cal.com booking page. The booking link is: https://cal.com/harsh-kumar-lodmok/15min

Important: Only use information from the retrieved context. Do not hallucinate or fabricate details.
If the context doesn't contain enough info to answer, be upfront about it."""


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def load_documents():
    """Load all documents from the data directory."""
    documents = []
    splitter = get_text_splitter()

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        return documents

    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = filename
                doc.metadata["type"] = "resume"
            documents.extend(splitter.split_documents(docs))
        elif filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = filename
                if "github" in filename.lower():
                    doc.metadata["type"] = "github"
                else:
                    doc.metadata["type"] = "resume"
            documents.extend(splitter.split_documents(docs))

    return documents


def init_vectorstore():
    """Initialize or load the vector store."""
    global vectorstore

    documents = load_documents()
    if not documents:
        print("WARNING: No documents found in data directory. RAG will not work.")
        return

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    print(f"Indexed {len(documents)} document chunks into vector store.")


def retrieve_context(query: str, k: int = 5, clean: bool = False) -> str:
    """Retrieve relevant context from the vector store.

    Args:
        query: The search query.
        k: Number of chunks to retrieve.
        clean: If True, return only page content without source metadata (for voice).
    """
    if vectorstore is None:
        return "No documents have been indexed yet."

    docs = vectorstore.similarity_search(query, k=k)
    context_parts = []
    for doc in docs:
        if clean:
            context_parts.append(doc.page_content)
        else:
            source = doc.metadata.get("source", "unknown")
            doc_type = doc.metadata.get("type", "unknown")
            context_parts.append(f"[Source: {source} | Type: {doc_type}]\n{doc.page_content}")

    return "\n\n---\n\n".join(context_parts)


def chat(session_id: str, user_message: str) -> dict:
    """Process a chat message and return a response with sources."""
    if session_id not in session_histories:
        session_histories[session_id] = []

    history = session_histories[session_id]

    # Retrieve relevant context
    context = retrieve_context(user_message)

    # Build messages for the LLM
    history_text = ""
    for msg in history[-10:]:  # Last 10 messages for context window
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Context from resume and GitHub:
{context}

Previous conversation:
{history_text}

User's question: {user_message}

Respond naturally as the AI persona. Be specific and grounded in the provided context."""),
    ]

    response = llm.invoke(messages)
    assistant_message = response.content

    # Update history
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_message})

    return {
        "response": assistant_message,
        "sources": _extract_sources(context),
    }


def _extract_sources(context: str) -> list[str]:
    """Extract source names from context."""
    sources = set()
    for line in context.split("\n"):
        if line.startswith("[Source:"):
            source = line.split("|")[0].replace("[Source:", "").strip()
            sources.add(source)
    return list(sources)
