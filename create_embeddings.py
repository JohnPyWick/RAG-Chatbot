import os
import pymongo
import requests

mongo_uri = os.getenv("MONGO_URI")
hf_token = os.getenv("HF_TOKEN")

client = pymongo.MongoClient(mongo_uri)
db = client.sample_mflix
collection = db.movies


embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"



def generate_embeddings(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers = {"Authorization": f"Bearer {hf_token}"},
        json= {"inputs": text}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}:{response.text}")
    
    return response.json()

    
for doc in collection.find({'plot': {"$exists": True}}).limit(5):
    doc['plot_embedding_hf'] = generate_embeddings(doc['plot'])
    collection.replace_one({'_id': doc['_id']}, doc)

