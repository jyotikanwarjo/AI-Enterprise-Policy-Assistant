import json
import fitz
from pathlib import Path
from chunking import create_chunks


DOCUMENTS_FOLDER = Path("Documents")


def process_pdf(pdf_path):
    all_chunks = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            if not text.strip():
                continue

            chunks = create_chunks(
                text,
                chunk_size=100,
                overlap=20
            )

            for chunk_index, chunk_text in enumerate(chunks, start=1):
                all_chunks.append({
                    "chunk_id": (
                        f"{pdf_path.stem}_page{page_number}"
                        f"_chunk{chunk_index}"
                    ),
                    "source": pdf_path.name,
                    "page": page_number,
                    "text": chunk_text
                })

    return all_chunks


def process_all_documents():
    all_chunks = []

    pdf_files = sorted(DOCUMENTS_FOLDER.glob("*.pdf"))

    for pdf_path in pdf_files:
        chunks = process_pdf(pdf_path)
        all_chunks.extend(chunks)

        print(f"Processed: {pdf_path.name}")
        print(f"Chunks created: {len(chunks)}\n")

    return all_chunks


if __name__ == "__main__":
    chunks = process_all_documents()

    output_path = Path("Knowledge/chunks.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=4, ensure_ascii=False)

    print("=" * 50)
    print(f"Total PDFs processed: {len(list(DOCUMENTS_FOLDER.glob('*.pdf')))}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Saved to: {output_path}")
    print("=" * 50)