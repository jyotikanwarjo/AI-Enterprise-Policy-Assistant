def create_chunks(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunks.append(" ".join(chunk_words))

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":
    sample_text = """
    Access Management Policy.
    Standard access requires manager approval.
    Privileged access requires manager approval,
    application-owner approval, and security review.
    Temporary access must have an expiry date.
    """

    chunks = create_chunks(
        sample_text,
        chunk_size=15,
        overlap=3
    )

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}:")
        print(chunk)