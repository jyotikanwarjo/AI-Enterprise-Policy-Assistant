import json
from pathlib import Path

import fitz


CHUNKS_FILE = Path("Knowledge/chunks.json")
DOCUMENTS_DIR = Path("Documents")


def main():
    if not CHUNKS_FILE.is_file():
        raise FileNotFoundError(
            f"Missing chunks file: {CHUNKS_FILE}"
        )

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("The chunks JSON is empty or invalid.")

    errors = []
    chunk_ids = set()
    page_counts = {}
    source_counts = {}

    for index, chunk in enumerate(chunks, start=1):
        if not isinstance(chunk, dict):
            errors.append(f"Record {index} is not a dictionary.")
            continue

        chunk_id = chunk.get("chunk_id")
        source = chunk.get("source")
        page = chunk.get("page")
        text = chunk.get("text")

        if not chunk_id:
            errors.append(f"Record {index} has no chunk_id.")
        elif chunk_id in chunk_ids:
            errors.append(f"Duplicate chunk ID: {chunk_id}")
        else:
            chunk_ids.add(chunk_id)

        if not isinstance(text, str) or not text.strip():
            errors.append(f"Record {index} has missing text.")

        if not isinstance(source, str) or not source:
            errors.append(f"Record {index} has invalid source.")
            continue

        pdf_path = DOCUMENTS_DIR / source

        if not pdf_path.is_file():
            errors.append(
                f"Record {index} references missing PDF: {source}"
            )
            continue

        source_counts[source] = source_counts.get(source, 0) + 1

        if (
            not isinstance(page, int)
            or isinstance(page, bool)
            or page < 1
        ):
            errors.append(
                f"Record {index} has invalid page number: {page}"
            )
            continue

        try:
            if source not in page_counts:
                with fitz.open(pdf_path) as pdf:
                    page_counts[source] = pdf.page_count

            if page > page_counts[source]:
                errors.append(
                    f"Record {index}: page {page} exceeds "
                    f"{source}'s {page_counts[source]} pages."
                )

        except Exception as error:
            errors.append(
                f"Could not inspect {source}: {error}"
            )

    print("=" * 55)
    print("DOCUMENT METADATA VALIDATION")
    print("=" * 55)
    print(f"Total chunks: {len(chunks)}")
    print(f"Unique chunk IDs: {len(chunk_ids)}")
    print(f"Documents referenced: {len(source_counts)}")

    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count} chunks")

    if errors:
        print(f"\nValidation errors: {len(errors)}")

        for error in errors:
            print("-", error)

        raise SystemExit(1)

    print("\nResult: PASS")
    print("All chunk source and page references are valid.")


if __name__ == "__main__":
    main()