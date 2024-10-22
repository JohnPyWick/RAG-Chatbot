Certainly! Below is a structured documentation for your RAG Chatbot project, which outlines the setup, usage, and components of the application.

---

# RAG Chatbot Documentation

## Overview

The RAG Chatbot is designed to perform semantic search using embeddings on movie plots stored in a MongoDB database. It utilizes the Hugging Face API to generate embeddings and the OpenAI API to generate conversational responses based on search results. The app is built with Streamlit, providing a user-friendly interface for querying and interacting with the chatbot.

## Features

- **Semantic Search**: Uses embeddings to find relevant movie plots from a database based on user queries.
- **Conversational AI**: Leverages OpenAI's GPT-4 model to provide insights or recommendations based on search results.
- **Interactive UI**: Built with Streamlit for easy user interaction.

## Prerequisites

- Python 3.7 or higher
- MongoDB Atlas account
- OpenAI API key
- Hugging Face API key

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd rag-chatbot
```

### Install Dependencies

All required dependencies are listed in the `requirements.txt` file. Use the following command to install them:

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### MongoDB Setup

1. **Create a MongoDB Cluster**: Sign up on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a cluster.

2. **Use Sample Movies Database**: Select the `sample_mflix` database, which includes a collection of movie plots.

3. **Update Connection String**: Ensure your MongoDB connection string is updated with your credentials. The format should be:

   ```plaintext
   mongodb+srv://<username>:<password>@cluster0.xjgh64a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```

### Running the Application

1. **Test MongoDB Connection**

   Use the `testmongodb.py` script to ensure connectivity with your MongoDB database.

   ```bash
   python testmongodb.py
   ```

2. **Create Plot Embeddings**

   Generate embeddings for the movie plots using the `create_embeddings.py` script:

   ```bash
   python create_embeddings.py
   ```

3. **Test Vector Search**

   Verify the semantic search functionality with `test_vector_search.py`:

   ```bash
   python test_vector_search.py
   ```

4. **Launch the Streamlit App**

   Run the main application using Streamlit:

   ```bash
   streamlit run chatai.py
   ```

   Enter a query in the input box and click on the "Search and Chat" button to see the results and get a response from ChatGPT.

## Code Structure

- **chatai.py**: Main script for running the Streamlit app, handling user input, and interacting with the OpenAI API.
- **create_embeddings.py**: Script for generating and storing embeddings for movie plots in the MongoDB database.
- **testmongodb.py**: Script for testing the MongoDB connection.
- **test_vector_search.py**: Script for testing the semantic search functionality.

## Streamlit Interface

- **Title**: Displays the application title.
- **Input Box**: Accepts user queries in natural language.
- **Search and Chat Button**: Initiates the semantic search and chat process.
- **Results Display**: Shows related movie plots and ChatGPT's response.

## Error Handling

The application includes error handling to manage potential issues such as:

- MongoDB connection errors
- API request failures
- Missing environment variables

## Contributing

Contributions are welcome! Please open an issue to discuss any major changes you wish to make. Pull requests should include relevant tests and documentation updates.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

Feel free to modify the documentation further based on specific project details or additional features you might implement.
