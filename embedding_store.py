import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

CHUNKS_FILE = Path("Knowledge/chunks.json")
DB_PATH = "Knowledge/chroma_db"
COLLECTION_NAME = "enterprise_policies"

chroma_client = chromadb.PersistentClient(path=DB_PATH)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


def generate_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_vector_store():
    chunks = load_chunks()

    # Remove previous records to avoid duplicate entries
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    batch_size = 20

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in batch:
            text = chunk["text"]

            embedding = generate_embedding(text)

            ids.append(chunk["chunk_id"])
            documents.append(text)
            embeddings.append(embedding)

            metadatas.append({
                "source": chunk["source"],
                "page": chunk["page"]
            })

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Stored {min(start + batch_size, len(chunks))}"
            f" of {len(chunks)} chunks"
        )

    print("\nVector database created successfully.")
    print("Total stored chunks:", collection.count())


if __name__ == "__main__":
    build_vector_store()