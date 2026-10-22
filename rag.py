
import os

from dotenv import load_dotenv
from google import genai

from semantic_search import search_documents


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


def generate_answer(question, results=None):
    """
    Generate an answer using retrieved enterprise policy chunks.

    If results are supplied, reuse them instead of searching again.
    """

    # Step 1: Retrieve relevant chunks if not already supplied
    if results is None:
        results = search_documents(question, top_k=4)

    # Step 2: Handle empty retrieval results
    if not results:
        return {
            "answer": (
                "I could not find relevant information in the "
                "available policy documents. Please consult the "
                "appropriate policy owner or Service Desk."
            ),
            "sources": []
        }

    # Step 3: Build context from retrieved chunks
    context_parts = []

    for item in results:
        context_parts.append(
            f"""
Source: {item.get('source', 'Unknown')}
Page: {item.get('page', 'Unknown')}

Content:
{item.get('text', '')}
"""
        )

    context = "\n\n".join(context_parts)

    # Step 4: Build a grounded prompt
    prompt = f"""
You are an enterprise policy and SOP assistant.

Answer the user's question using only the context provided below.

Rules:
1. Do not invent policy requirements or procedures.
2. Do not use outside knowledge to fill gaps.
3. If the context does not contain enough information,
   clearly state that the available documents do not specify it.
4. If the supplied documents conflict, explain the conflict.
5. Do not invent document names, page numbers, or citations.
6. The application will display source references separately.
7. Keep the answer clear and concise.

POLICY CONTEXT:
{context}

USER QUESTION:
{question}

Provide a grounded answer.
"""

    # Step 5: Generate the answer
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    answer = response.text

    if not answer:
        answer = (
            "The model did not return an answer. "
            "Please try again later."
        )

    # Step 6: Collect unique source references from metadata
    sources = []
    seen_sources = set()

    for item in results:
        source = item.get("source")
        page = item.get("page")

        if (
            not source
            or not isinstance(page, int)
            or isinstance(page, bool)
            or page < 1
        ):
            continue

        key = (source, page)

        if key not in seen_sources:
            sources.append({
                "source": source,
                "page": page
            })
            seen_sources.add(key)

    # Step 7: Return the answer and its source metadata
    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    question = input("Ask a policy question: ")

    result = generate_answer(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCE REFERENCES:")

    if result["sources"]:
        for source in result["sources"]:
            print(
                f"- {source['source']}, "
                f"Page {source['page']}"
            )
    else:
        print("No source references available.")
