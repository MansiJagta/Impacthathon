from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import collection


def generate_embedding(text):
    """Placeholder for text embedding logic."""
    # Since we are using TF-IDF in similarity search,
    # this might be used for other purposes later.
    return [0.0] * 128  # Dummy embedding


def find_similar_claims(query_text, claim_type, top_k=3):
    claims = list(collection.find({}))
    if not claims:
        return []

    documents = [claim.get("damage_description", "") for claim in claims]

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(documents + [query_text])
    except ValueError:
        return []

    similarities = cosine_similarity(
        tfidf_matrix[-1],  # query
        tfidf_matrix[:-1],  # historical
    )[0]

    results = []
    for idx, score in enumerate(similarities):
        results.append(
            {
                "claim_id": claims[idx].get("claim_id", "Unknown"),
                "final_cost": claims[idx].get("final_cost", 0),
                "similarity": float(score),
                "settlement_days": claims[idx].get("settlement_days", 0),
            }
        )

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
