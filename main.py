from fastapi import FastAPI
from pydantic import BaseModel
from ingest import get_embedding
import chromadb
import ollama

app = FastAPI()

class ChatRequest(BaseModel):
    # TODO: what field(s) do we need here? (hint: just the user's question, for now)
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    # TODO: for now, just return the question back to confirm it's working
    chunks = retrieve_chunks(request.question)
    prompt = build_prompt(request.question, chunks)
    answer = get_answer(prompt)
    return {"question": request.question, "answer": answer}

def retrieve_chunks(question, top_k=3):
    question_embedding = get_embedding(question)
    
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="netsol_docs")
    
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k     
    )
    
    return results["documents"][0]  # Return the documents of the top result

 
    
def build_prompt(question, chunks):
    context = "\n\n".join(chunks)
    
    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:"""

    return prompt

def get_answer(prompt):
    response = ollama.generate(model="llama3.2", prompt=prompt)
    answer = response["response"]
    return answer

if __name__ == "__main__":
    test_chunks = retrieve_chunks("What is netsol")
    test_prompt = build_prompt("What is netsol", test_chunks)
    test_answer = get_answer(test_prompt)
    print(test_answer)