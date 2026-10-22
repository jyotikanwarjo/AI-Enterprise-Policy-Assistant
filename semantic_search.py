import os

import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

chroma_client = chromadb.PersistentClient(
    path="Knowledge/chroma_db"
)

collection = chroma_client.get_collection(
    name="enterprise_policies"
)


def generate_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def search_documents(question, top_k=3):
    query_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []

    for index in range(len(results["ids"][0])):
        matches.append({
            "text": results["documents"][0][index],
            "source": results["metadatas"][0][index]["source"],
            "page": results["metadatas"][0][index]["page"],
            "distance": results["distances"][0][index]
        })

    return matches


if __name__ == "__main__":
    question = input("Enter your question: ")

    results = search_documents(question)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Distance:", result["distance"])
        print("Text:", result["text"])