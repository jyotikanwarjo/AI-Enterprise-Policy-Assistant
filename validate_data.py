import json
from pathlib import Path

json_path = Path("Knowledge/chunks.json")

with open(json_path, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Total chunks:", len(chunks))

sources = set()
missing_text = 0
missing_metadata = 0

for chunk in chunks:
    sources.add(chunk.get("source"))

    if not chunk.get("text", "").strip():
        missing_text += 1

    if not chunk.get("source") or not chunk.get("page"):
        missing_metadata += 1

print("Unique documents:", len(sources))
print("Missing text:", missing_text)
print("Missing metadata:", missing_metadata)

print("\nDocuments found:")

for source in sorted(sources):
    print("-", source)