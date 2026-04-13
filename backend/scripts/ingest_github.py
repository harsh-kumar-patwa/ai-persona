"""Fetch GitHub repos and generate a document for RAG ingestion."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.github_service import generate_github_document
from app.config import DATA_DIR


async def main():
    print("Fetching GitHub repos...")
    document = await generate_github_document()

    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "github_repos.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(document)

    print(f"GitHub document saved to {output_path}")
    print(f"Document length: {len(document)} characters")


if __name__ == "__main__":
    asyncio.run(main())
