from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Don't load the model immediately
model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def get_match_score(resume_text, jd_text):
    """
    Returns similarity score between resume and job description.
    """

    model = get_model()

    embeddings = model.encode([resume_text, jd_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(score) * 100, 2)