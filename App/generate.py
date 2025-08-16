import os
from dotenv import load_dotenv
from pinecone import Pinecone
from together import Together

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_IDX_NAME")

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

client = Together(api_key=TOGETHER_API_KEY)

def search_similar_chunks(query, top_k=5):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vector = model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    chunks = []
    for match in results['matches']:
        metadata = match['metadata']
        title = metadata.get('title', 'No Title')
        description = metadata.get('description', 'No Description')
        url = metadata.get('url', 'No URL')
        chunks.append(f" {title}\n {description}\n {url}\n")
    return "\n".join(chunks)

def generate_answer(context, user_prompt):
    full_prompt = f"Answer the following using the given context.\n\nContext:\n{context}\n\nQuestion:\n{user_prompt}"
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role":"user","content":full_prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_prompt = input("Enter your question: ")
    context = search_similar_chunks(user_prompt)
    answer = generate_answer(context, user_prompt)
    print("\n Answer:\n", answer)