from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(stop_words="english")

def get_match_score(resume_text, jd_text):
    tfidf = vectorizer.fit_transform([resume_text, jd_text])

    score = cosine_similarity(
        tfidf[0:1],
        tfidf[1:2]
    )[0][0]

    return round(score * 100, 2)