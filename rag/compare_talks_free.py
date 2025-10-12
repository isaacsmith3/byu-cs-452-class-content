import pandas as pd  # type: ignore
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

# Load the same model used for generating embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

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


def compare_content(talks_df, paragraphs_df, clusters_df):
    """
    Compare the questions against talks, paragraphs, and clusters to find top 3 matches.

    Args:
        talks_df: DataFrame of talks with embeddings
        paragraphs_df: DataFrame of paragraphs with embeddings
        clusters_df: DataFrame of clusters with embeddings
    """

    # Generate embeddings for questions
    question_embeddings = model.encode(questions)

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
    free_talks = pd.read_csv("free/free_talks.csv")
    free_paragraphs = pd.read_csv("free/free_paragraphs.csv")
    free_3_clusters = pd.read_csv("free/free_3_clusters.csv")

    print("Running similarity search on free embeddings...")
    free_results = compare_content(free_talks, free_paragraphs, free_3_clusters)

    print("\n" + "=" * 80)
    print(
        "Note: OpenAI embeddings use a different model (1536 dimensions) than the free embeddings (384 dimensions)."
    )
    print(
        "To compare OpenAI embeddings, you would need to use the same OpenAI model that generated them."
    )
    print(
        "The free embeddings comparison above shows the results using the all-MiniLM-L6-v2 model."
    )
