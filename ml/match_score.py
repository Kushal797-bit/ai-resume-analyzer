from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_match_score(resume_text, jd_text):
    """
    Returns similarity score between resume and job description.
    """

    embeddings = model.encode([resume_text, jd_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    match_percent = round(float(score) * 100, 2)

    return match_percent