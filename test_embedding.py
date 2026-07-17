# test_embedding.py
from ingest import chunk_text, get_embedding

with open("data/raw/homepage.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text)
first_chunk = chunks[0]

embedding = get_embedding(first_chunk)
print("Chunk preview:", first_chunk[:80])
print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])