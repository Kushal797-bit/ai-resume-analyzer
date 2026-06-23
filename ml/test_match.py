from match_score import get_match_score

resume = """
Experienced Python developer skilled in Flask,
REST APIs, Docker and Machine Learning.
"""

jd1 = """
Looking for a backend engineer with Python,
Flask and Machine Learning experience.
"""

jd2 = """
Looking for an experienced chef with restaurant
management skills.
"""

print("Related JD Score:")
print(get_match_score(resume, jd1))

print("\nUnrelated JD Score:")
print(get_match_score(resume, jd2))