import os
from dotenv import load_dotenv
from pinecone import Pinecone
from ibm_watson_machine_learning import APIClient

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_IDX_NAME")

IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

wml_credentials = {
    "apikey": IBM_API_KEY,
    "url": "https://us-south.ml.cloud.ibm.com"  
}

client = APIClient(wml_credentials)
client.set.default_project(IBM_PROJECT_ID)  

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
    payload = {
        "model_id": "meta-llama/llama-3-8b-instruct",  # or 70B if available
        "inputs": full_prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 500,
            "stop_sequences": ["</s>"]
        }
    }
    response = client.generate_text(payload)
    return response['results'][0]['generated_text']

if __name__ == "__main__":
    user_prompt = input("Enter your question: ")
    context = search_similar_chunks(user_prompt)
    answer = generate_answer(context, user_prompt)
    print("\n Answer:\n", answer)