import pymongo
import requests
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

mongo_uri = os.getenv("MONGO_URI")
hf_token = os.getenv("HF_TOKEN") # Hugging Face API credentials

# MongoDB client setup
client = pymongo.MongoClient(mongo_uri)
db = client.sample_mflix
collection = db.movies


# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
# Initialize OpenAI client with your API key
openai_client = OpenAI(api_key=openai_api_key)  # Replace with your OpenAI API key

# URL for the Hugging Face embedding model
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

# Function to generate embeddings from text using Hugging Face API
def generate_embeddings(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

# Function to query the OpenAI API for a chat response
def chat_with_openai(prompt: str) -> str:
    completion = openai_client.chat.completions.create(
        model="gpt-4o",  # Update model name if necessary
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Only provide insights or recommendations based on the given list of movies."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    return completion.choices[0].message.content.strip()

# Streamlit UI setup
st.title("Movie Plot Semantic Search and Chat")
st.write("Enter a query to find related movie plots and get insights from ChatGPT.")

# User input
query = st.text_input("Enter your query:","lost in forest and trying to survive")

if st.button("Search and Chat"):
    # Retrieve relevant documents from MongoDB using semantic search
    try:
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "queryVector": generate_embeddings(query),
                    "path": "plot_embedding_hf",
                    "numCandidates": 100,
                    "limit": 4,
                    "index": "PlotSemanticSearch",
                }
            }
        ])

        # Prepare the results into a single text prompt
        prompt = f"User query: {query}\n\nHere are some movies related to your query. Only use these to provide insights or recommendations:\n"
        movie_list = []
        for document in results:
            movie_list.append(document)
            prompt += f"Movie Name: {document['title']}\nMovie Plot: {document['plot']}\n\n"

        # Get response from OpenAI
        response = chat_with_openai(prompt)

        # Display the results and ChatGPT response
        st.subheader("Movie Results")
        for document in movie_list:
            st.write(f"**Movie Name:** {document['title']}")
            st.write(f"**Movie Plot:** {document['plot']}\n")

        st.subheader("ChatGPT Response")
        st.write(response)

    except Exception as e:
        st.error(f"An error occurred: {e}")
