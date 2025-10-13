import pandas as pd  # type: ignore
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load OpenAI client
with open("config.json") as config:
    openaiKey = json.load(config)["openaiKey"]

client = OpenAI(api_key=openaiKey)

# Static questions for testing
questions = [
    "How can I gain a testimony of Jesus Christ?",
    "What are some ways to deal with challenges in life and find a purpose?",
    "How can I fix my car if it won't start?",  # funny test question
]


def parse_embedding(embedding_str):
    """Parse embedding string to numpy array"""
    if isinstance(embedding_str, str):
        return np.array(eval(embedding_str))
    return embedding_str


def get_question_embeddings(questions, model="text-embedding-3-small"):
    """
    Generate OpenAI embeddings for questions.

    Args:
        questions: List of question strings
        model: OpenAI embedding model name

    Returns:
        List of numpy arrays containing embeddings
    """
    response = client.embeddings.create(input=questions, model=model)
    embeddings = [np.array(item.embedding) for item in response.data]
    return embeddings


def find_best_cluster(question_embedding, clusters_df):
    """
    Find the best cluster match for a question using cosine similarity.

    Args:
        question_embedding: numpy array of question embedding
        clusters_df: DataFrame with cluster embeddings

    Returns:
        Best matching cluster row with similarity score
    """
    # Parse embeddings
    embeddings = clusters_df["embedding"].apply(parse_embedding).tolist()
    embeddings_matrix = np.array(embeddings)

    # Calculate cosine similarities
    similarities = cosine_similarity([question_embedding], embeddings_matrix)[0]

    # Add similarity scores to dataframe
    clusters_df_copy = clusters_df.copy()
    clusters_df_copy["similarity"] = similarities

    # Return the best match
    best_match = clusters_df_copy.nlargest(1, "similarity").iloc[0]
    return best_match


def format_retrieved_content(cluster_row):
    """
    Format the retrieved cluster content for the prompt.

    Args:
        cluster_row: Best matching cluster from find_best_cluster

    Returns:
        Formatted string with cluster information
    """
    # Extract cluster text (it's stored as a list of strings)
    cluster_text = cluster_row["text"]
    if isinstance(cluster_text, str):
        # If it's a string representation of a list, evaluate it
        cluster_text = eval(cluster_text)

    # Join the paragraphs with proper formatting
    formatted_text = "\n\n".join(cluster_text)

    return f"""
Title: {cluster_row['title']}
Speaker: {cluster_row['speaker']}
Year: {cluster_row['year']}, {cluster_row['season']}
Similarity Score: {cluster_row['similarity']:.4f}

Relevant Content:
{formatted_text}
"""


def generate_response_with_chatgpt(question, retrieved_content):
    """
    Generate a response using ChatGPT with the retrieved content as context.

    Args:
        question: The user's question
        retrieved_content: Formatted content from the best matching cluster

    Returns:
        Generated response from ChatGPT
    """
    prompt = f"""You are a helpful assistant that answers questions based on Latter-day Saint conference talks. 
Use the provided conference talk content to give thoughtful, accurate answers that are grounded in the teachings of the Church of Jesus Christ of Latter-day Saints.

Question: {question}

Relevant Conference Talk Content:
{retrieved_content}

Please provide a comprehensive answer based on the conference talk content above. Make sure to:
1. Directly reference the teachings and examples from the conference talk
2. Provide practical insights and applications
3. Maintain the spiritual and doctrinal context
4. Be encouraging and uplifting in your response

Answer:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions about Latter-day Saint teachings using conference talk content.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return f"Error generating response: {e}"


def run_rag_system():
    """
    Run the complete RAG system: Retrieve best clusters and generate responses.
    """
    print("=" * 80)
    print("RAG SYSTEM: Retrieval-Augmented Generation with ChatGPT")
    print("=" * 80)

    # Load cluster embeddings data
    print("Loading cluster embeddings...")
    openai_3_clusters = pd.read_csv("openai/openai_3_clusters.csv")

    # Generate embeddings for questions
    print("Generating question embeddings...")
    question_embeddings = get_question_embeddings(questions)

    print("Running RAG system...\n")

    for i, question in enumerate(questions):
        print(f"Question {i+1}: {question}")
        print("-" * 60)

        # Step 1: Retrieval - Find best cluster
        question_embedding = question_embeddings[i]
        best_cluster = find_best_cluster(question_embedding, openai_3_clusters)

        print(f"Retrieved: {best_cluster['title']} by {best_cluster['speaker']}")
        print(f"Similarity Score: {best_cluster['similarity']:.4f}")

        # Step 2: Generation - Create response with ChatGPT
        retrieved_content = format_retrieved_content(best_cluster)
        generated_response = generate_response_with_chatgpt(question, retrieved_content)

        print("\nGenerated Response:")
        print("-" * 40)
        print(generated_response)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    run_rag_system()
