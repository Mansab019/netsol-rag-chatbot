import ollama
import chromadb
import os


def chunk_text(text, chunk_size = 500, overlap = 50):
    """
    Splits the input text into chunks of specified size with a given overlap.
    
    Parameters:
    - text (str): The input text to be chunked.
    - chunk_size (int): The maximum size of each chunk. Default is 500 characters.
    - overlap (int): The number of overlapping characters between consecutive chunks. Default is 50 characters.
    
    Returns:
    - List[str]: A list of text chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Move the start index forward by chunk_size minus overlap
        start += chunk_size - overlap
    
    return chunks



    

def get_embedding(text):
    """
    Generates an embedding for the given text using the Ollama API.

    Parameters:
    - text (str): The input text for which the embedding is to be generated.

    Returns:
    - List[float]: The embedding vector.
    """
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


def store_in_chroma():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name = "netsol_docs")
    
    raw_folder = "data/raw"
    for filename in os.listdir(raw_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(raw_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                embedding = get_embedding(chunk)
                collection.add(
                    ids=[f"{filename}_{i}"],
                    documents=[chunk],
                    metadatas=[{"source": filename, "chunk_index": i}],
                    embeddings=[embedding]
                )
            print(f"Processed and stored: {filename} with {len(chunks)} chunks.")

    # loop through data/raw/*.txt
    # for each file: chunk_text() -> get_embedding() -> collection.add(...)
    # 
if __name__ == "__main__":
    with open("data/raw/homepage.txt", "r", encoding="utf-8") as f:
        text = f.read()
    store_in_chroma()
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")
    print(f"First chunk:\n{chunks[0]}")
    print(f"\nSecond chunk:\n{chunks[1]}")
   