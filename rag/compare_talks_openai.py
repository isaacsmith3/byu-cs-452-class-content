import pandas as pd  # type: ignore
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
import json

# Load OpenAI client
with open("config.json") as config:
    openaiKey = json.load(config)["openaiKey"]

client = OpenAI(api_key=openaiKey)

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


def find_top_matches(question_embedding, content_df, top_k=3):
    """
    Find top k most similar content items using cosine similarity.

    Args:
        question_embedding: numpy array of question embedding
        content_df: DataFrame with 'embedding' column
        top_k: number of top matches to return

    Returns:
        DataFrame with top k matches including similarity scores
    """
    # Parse embeddings
    embeddings = content_df["embedding"].apply(parse_embedding).tolist()
    embeddings_matrix = np.array(embeddings)

    # Calculate cosine similarities
    similarities = cosine_similarity([question_embedding], embeddings_matrix)[0]

    # Add similarity scores to dataframe
    content_df_copy = content_df.copy()
    content_df_copy["similarity"] = similarities

    # Sort by similarity and return top k
    top_matches = content_df_copy.nlargest(top_k, "similarity")

    return top_matches


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


def compare_content(talks_df, paragraphs_df, clusters_df):
    """
    Compare the questions against talks, paragraphs, and clusters to find top 3 matches.

    Args:
        talks_df: DataFrame of talks with embeddings
        paragraphs_df: DataFrame of paragraphs with embeddings
        clusters_df: DataFrame of clusters with embeddings
    """

    # Generate embeddings for questions using OpenAI API
    question_embeddings = get_question_embeddings(questions)

    results = {}

    for i, question in enumerate(questions):
        print(f"\n=== Question {i+1}: {question} ===")

        question_embedding = question_embeddings[i]

        # Find top matches for each content type
        top_talks = find_top_matches(question_embedding, talks_df)
        top_paragraphs = find_top_matches(question_embedding, paragraphs_df)
        top_clusters = find_top_matches(question_embedding, clusters_df)

        results[question] = {
            "talks": top_talks,
            "paragraphs": top_paragraphs,
            "clusters": top_clusters,
        }

        # Print results
        print("\nTop 3 Talks:")
        for idx, row in top_talks.iterrows():
            print(
                f"  {row['title']} by {row['speaker']} (similarity: {row['similarity']:.4f})"
            )
            print(f"    Text preview: {row['text'][:200]}...")

        print("\nTop 3 Paragraphs:")
        for idx, row in top_paragraphs.iterrows():
            print(
                f"  {row['title']} by {row['speaker']} (similarity: {row['similarity']:.4f})"
            )
            print(f"    Text: {row['text'][:200]}...")

        print("\nTop 3 Clusters:")
        for idx, row in top_clusters.iterrows():
            print(
                f"  {row['title']} by {row['speaker']} (similarity: {row['similarity']:.4f})"
            )
            print(f"    Text: {row['text'][:200]}...")

    return results


if __name__ == "__main__":
    # Load free embeddings data
    openai_talks = pd.read_csv("openai/openai_talks.csv")
    openai_paragraphs = pd.read_csv("openai/openai_paragraphs.csv")
    openai_3_clusters = pd.read_csv("openai/openai_3_clusters.csv")

    print("Running similarity search on openai embeddings...")
    openai_results = compare_content(openai_talks, openai_paragraphs, openai_3_clusters)

    print("\n" + "=" * 80)
    print("OpenAI embeddings comparison completed successfully!")
    print(
        "Results show the top 3 matches for each question using OpenAI's text-embedding-3-small model (1536 dimensions)."
    )
