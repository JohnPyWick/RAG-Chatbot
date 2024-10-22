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

    
query = "a man goes at war"

results = collection.aggregate([
    {
        "$vectorSearch": {
            "queryVector": generate_embeddings(query),
            "path": "plot_embedding_hf",
            "numCandidates":100,
            "limit": 4,
            "index": "PlotSemanticSearch",
        }
    }
]);

print(results)

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')
