import chromadb
from ingest import get_embedding

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="netsol_docs")

question = "What are NETSOL's Q2 2026 earnings?"
question_embedding = get_embedding(question)

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

print(results["documents"])