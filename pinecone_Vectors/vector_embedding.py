import os
import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not not PINECONE_API_KEY:
    raise ValueError("API key for Pinecone must be set in the .env file.")

pc = Pinecone(api_key=PINECONE_API_KEY)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384
index_name = "coursera-courses"

print("Successfully connected to Pinecone!")

if index_name not in pc.list_indexes().names():
    print(f"Creating index '{index_name}' with dimension {EMBEDDING_DIMENSION}...")
    pc.create_index(
        name=index_name,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine"
    )
    print("Index created successfully.")
else:
    print(f"Index '{index_name}' already exists.")

index = pc.Index(index_name)



try:
    with open("coursera_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise TypeError("JSON file is not a list of courses.")
except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
    print(f"Error loading or parsing coursera_data.json: {e}")
    exit()

seen_ids = set()
unique_data = []
for item in data:
    uid = item.get("uuid")
    if isinstance(item, dict) and uid and uid not in seen_ids:
        unique_data.append(item)
        seen_ids.add(uid)

print(f"Original items: {len(data)}, Unique items: {len(unique_data)}")

batch_size = 50
for i in tqdm(range(0, len(unique_data), batch_size)):
    batch = unique_data[i:i+batch_size]

    ids = [item["uuid"] for item in batch]
    texts = [f"{item.get('name', '')}: {item.get('description', '')}" for item in batch]

    embeddings = embedding_model.encode(texts).tolist()

    metadata = [
        {
            "title": item.get("name", ""),
            "description": item.get("description", ""),
            "url": item.get("course_url", ""),
            "platform": "Coursera"
        }
        for item in batch
    ]

    vectors_to_upsert = [
        {
            "id": ids[j],
            "values": embeddings[j],
            "metadata": metadata[j]
        }
        for j in range(len(ids))
    ]

    try:
        result = index.upsert(vectors=vectors_to_upsert)
        print(f"Upserted {len(vectors_to_upsert)} vectors.")
    except Exception as e:
        print(f"Failed to upsert batch {i // batch_size + 1}: {e}")

print("Embeddings created and stored in Pinecone successfully.")
print(index.describe_index_stats())




