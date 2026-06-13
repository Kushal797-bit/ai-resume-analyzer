import spacy

# Load spaCy model once at import time
# Run this in terminal first if not installed:
#   python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError(
        "spaCy model not found. Run:  python -m spacy download en_core_web_sm"
    )


def lemmatize(text):
    """
    Converts text to lowercase lemmas.
    e.g. "developing APIs" → ["develop", "api"]
    This means "developed", "developing", "developer" all match "develop".
    """
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc])


def extract_skills(text, skills_list):
    """
    Extracts skills from resume/JD text using spaCy lemmatization.
    More accurate than plain string matching — handles word variations.
    """
    lemmatized_text = lemmatize(text)
    found_skills = []

    for skill in skills_list:
        lemmatized_skill = lemmatize(skill)
        if lemmatized_skill in lemmatized_text:
            found_skills.append(skill)

    return found_skills


def predict_job_role(skills, job_roles):
    best_match = None
    highest_score = 0
    for role, required_skills in job_roles.items():
        score = 0
        for skill in skills:
            if skill in required_skills:
                score += required_skills[skill]
        if score > highest_score:
            highest_score = score
            best_match = role
    return best_match


def get_top_roles(skills, job_roles):
    role_scores = {}
    for role, required_skills in job_roles.items():
        score = 0
        for skill in skills:
            if skill in required_skills:
                score += required_skills[skill]
        role_scores[role] = score

    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_roles[:3]


def calculate_ats_score(skills, required_skills):
    total_required_skills = len(required_skills)
    if total_required_skills == 0:
        return 0
    matched_skills = len(set(skills) & set(required_skills))
    score = (matched_skills / total_required_skills) * 100
    return round(score, 2)


def find_missing_skills(skills, required_skills):
    return list(set(required_skills) - set(skills))


def check_resume_length(text):
    """
    Checks word count and returns a warning if too short or too long.
    Recruiters prefer resumes between 200 and 800 words.
    Returns a dict: { "word_count": int, "warning": str or None }
    """
    word_count = len(text.split())

    if word_count < 200:
        warning = (
            f"Your resume is very short ({word_count} words). "
            "Most recruiters expect at least 200 words. "
            "Add more detail to your experience and projects."
        )
    elif word_count > 800:
        warning = (
            f"Your resume is quite long ({word_count} words). "
            "Try to keep it under 800 words — recruiters spend only 6–10 seconds on a first scan."
        )
    else:
        warning = None

    return {"word_count": word_count, "warning": warning}




SECTION_KEYWORDS = {
    "Education": [
        "education", "academic background", "qualifications",
        "degree", "university", "college", "school", "b.tech",
        "b.sc", "m.tech", "m.sc", "bachelor", "master"
    ],
    "Work Experience": [
        "experience", "work experience", "employment history",
        "internship", "intern", "worked at", "job history",
        "professional experience", "career"
    ],
    "Projects": [
        "projects", "project", "personal projects",
        "academic projects", "key projects", "built", "developed"
    ],
    "Skills": [
        "skills", "technical skills", "core competencies",
        "technologies", "tools", "tech stack", "expertise"
    ],
    "Certifications": [
        "certification", "certifications", "certified",
        "certificate", "courses", "coursework", "udemy",
        "coursera", "nptel", "credential"
    ],
    "Achievements": [
        "achievement", "achievements", "accomplishments",
        "awards", "honors", "recognition", "winner"
    ],
    "Summary / Objective": [
        "summary", "objective", "profile", "about me",
        "career objective", "professional summary", "overview"
    ],
}

SECTION_TIPS = {
    "Education": "Add an Education section with your degree, college name, and graduation year.",
    "Work Experience": "Add internships or part-time roles. Even a 1-month internship counts.",
    "Projects": "Add 2-3 projects with a one-line description and the tech stack used.",
    "Skills": "Add a dedicated Skills section listing your programming languages, tools, and frameworks.",
    "Certifications": "Add any online certifications (Coursera, Udemy, NPTEL). They strengthen your profile.",
    "Achievements": "Add hackathon wins, rank in class, or any academic recognition.",
    "Summary / Objective": "Add a 2-3 line summary at the top saying who you are and what role you are targeting.",
}


def detect_resume_sections(resume_text):
    text_lower = resume_text.lower()
    results = []
    for section, keywords in SECTION_KEYWORDS.items():
        found = any(kw in text_lower for kw in keywords)
        results.append({
            "section": section,
            "present": found,
            "tip": "" if found else SECTION_TIPS.get(section, "")
        })
    return results

RADAR_DOMAINS = {
    "ML/AI": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "reinforcement learning", "transfer learning",
        "generative ai", "large language models", "llm", "transformers",
        "bert", "gpt", "scikit-learn", "tensorflow", "keras", "pytorch",
        "xgboost", "lightgbm", "hugging face", "spacy", "nltk",
        "supervised learning", "unsupervised learning"
    ],
    "Data": [
        "pandas", "numpy", "matplotlib", "seaborn", "plotly",
        "sql", "excel", "power bi", "tableau", "data science",
        "data analysis", "data visualization", "statistics",
        "time series analysis", "forecasting", "a/b testing",
        "feature engineering", "data engineering", "etl"
    ],
    "Programming": [
        "python", "java", "c++", "c", "javascript", "typescript",
        "r", "scala", "go", "rust", "bash", "shell scripting"
    ],
    "Backend": [
        "flask", "django", "fastapi", "nodejs", "expressjs",
        "rest api", "graphql", "grpc", "microservices",
        "mysql", "postgresql", "mongodb", "redis", "firebase",
        "sqlalchemy", "celery"
    ],
    "Cloud/DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker",
        "kubernetes", "github actions", "ci/cd", "terraform",
        "jenkins", "nginx", "linux", "heroku", "vercel"
    ],
    "AI Tools": [
        "langchain", "llama index", "openai api", "gemini api",
        "anthropic api", "hugging face", "mlflow", "wandb",
        "airflow", "apache spark", "databricks", "snowflake",
        "vector database", "pinecone", "chromadb", "rag",
        "retrieval augmented generation", "prompt engineering",
        "fine tuning", "embeddings"
    ]
}


def calculate_radar_scores(detected_skills):
    """
    Takes the list of skills detected from a resume and returns
    a score (0–100) for each of the 6 radar domains.

    Returns a dict like:
    {
        "ML & AI": 65,
        "Data & Analytics": 40,
        "Programming": 80,
        "Backend & APIs": 55,
        "Cloud & DevOps": 20,
        "AI Tools & Frameworks": 30
    }
    """
    detected_lower = [s.lower() for s in detected_skills]
    scores = {}

    for domain, domain_skills in RADAR_DOMAINS.items():
        matched = sum(1 for s in domain_skills if s in detected_lower)
        total = len(domain_skills)
        scores[domain] = round((matched / total) * 100) if total > 0 else 0

    return scores

# ══════════════════════════════════════════════════════════════
# Paste this at the bottom of your skill_extractor.py
# ══════════════════════════════════════════════════════════════

SKILL_TIPS = {
    # Programming
    "python":         ("🐍", "Build a small automation script or data project and push it to GitHub."),
    "java":           ("☕", "Build a simple REST API using Spring Boot and host it on GitHub."),
    "c++":            ("⚙️", "Solve 20 LeetCode problems in C++ and mention it on your resume."),
    "javascript":     ("🌐", "Build a simple interactive webpage and host it free on GitHub Pages."),
    "typescript":     ("🔷", "Convert one of your JavaScript projects to TypeScript — shows maturity."),
    "go":             ("🐹", "Build a small CLI tool in Go — great for backend and DevOps roles."),
    "r":              ("📊", "Do a data analysis project in R on a Kaggle dataset and share it."),
    "scala":          ("🔥", "Build a simple Apache Spark pipeline in Scala for data engineering roles."),

    # ML / AI
    "machine learning":    ("🤖", "Complete Andrew Ng's ML course on Coursera and add the certificate."),
    "deep learning":       ("🧠", "Build an image classifier using PyTorch or TensorFlow and push to GitHub."),
    "nlp":                 ("💬", "Build a text classifier or sentiment analyser using spaCy or HuggingFace."),
    "computer vision":     ("👁️",  "Build an object detection project using OpenCV or YOLO and document it."),
    "tensorflow":          ("🔶", "Complete TensorFlow Developer Certificate — it's recognized by Google."),
    "pytorch":             ("🔥", "Rebuild a paper from scratch in PyTorch — even a simple one impresses."),
    "scikit-learn":        ("📐", "Add a full ML pipeline project (preprocessing → model → evaluation) to GitHub."),
    "keras":               ("🧬", "Build a CNN or RNN model in Keras with a clear README and results."),
    "transformers":        ("🤗", "Fine-tune a BERT model on a custom dataset using HuggingFace Transformers."),
    "hugging face":        ("🤗", "Use HuggingFace pipelines in a project — even a demo notebook counts."),
    "langchain":           ("🔗", "Build a simple RAG chatbot using LangChain and OpenAI — very in demand."),
    "large language models": ("🧠", "Build an LLM-powered app using LangChain or OpenAI API and demo it."),
    "rag":                 ("📚", "Build a document Q&A system using RAG — one of the hottest AI skills now."),
    "prompt engineering":  ("✍️",  "Study OpenAI's prompt engineering guide and add an LLM project to GitHub."),

    # Data
    "pandas":         ("🐼", "Do a full EDA project on a Kaggle dataset using Pandas and share the notebook."),
    "numpy":          ("🔢", "Add NumPy to your existing data projects — it pairs naturally with Pandas."),
    "matplotlib":     ("📈", "Add visualizations to your data projects — even simple plots matter."),
    "seaborn":        ("🎨", "Create a visual data story using Seaborn on any public dataset."),
    "sql":            ("🗄️",  "Complete SQLZoo or Mode Analytics SQL Tutorial — free and highly practical."),
    "power bi":       ("📊", "Build a dashboard on a public dataset and add a screenshot to your resume."),
    "tableau":        ("📉", "Create a free Tableau Public dashboard — it's visible to anyone online."),
    "data science":   ("🔬", "Start a Kaggle competition — even a bronze medal shows real experience."),
    "statistics":     ("📐", "Take a free statistics course on Khan Academy or Coursera and apply it in a project."),

    # Backend / APIs
    "flask":          ("🌶️",  "Build a REST API with Flask, add authentication, and deploy it free on Render."),
    "django":         ("🎸", "Build a full CRUD web app in Django with login/logout and deploy it."),
    "fastapi":        ("⚡", "Build a FastAPI project with Swagger docs — FastAPI is trending in AI backends."),
    "rest api":       ("🔌", "Add a REST API to one of your existing projects using Flask or FastAPI."),
    "mongodb":        ("🍃", "Add MongoDB to a Flask project — shows you can work with NoSQL databases."),
    "postgresql":     ("🐘", "Replace SQLite in one of your projects with PostgreSQL — shows production thinking."),
    "mysql":          ("🐬", "Build a project with MySQL and write optimized queries — mention it in your resume."),
    "redis":          ("⚡", "Add Redis caching to an existing API project — shows backend maturity."),
    "docker":         ("🐳", "Dockerize one of your existing projects — add a Dockerfile and docker-compose.yml."),

    # Cloud / DevOps
    "aws":            ("☁️",  "Get AWS Cloud Practitioner certification — it's entry level and highly recognized."),
    "azure":          ("🔵", "Complete AZ-900 Microsoft Azure Fundamentals — free study materials available."),
    "gcp":            ("🌈", "Try Google Cloud free tier — deploy a Flask app on Cloud Run for your resume."),
    "kubernetes":     ("☸️",  "Learn Kubernetes basics on Killercoda.com — free browser-based practice."),
    "github actions": ("⚙️", "Add a CI/CD pipeline to one of your GitHub repos using GitHub Actions."),
    "ci/cd":          ("🔄", "Set up a GitHub Actions workflow that tests and deploys your app automatically."),
    "linux":          ("🐧", "Use WSL2 on Windows or a free Linux VM to practice shell commands daily."),
    "terraform":      ("🏗️",  "Write a Terraform script to provision an AWS EC2 instance — add it to GitHub."),
    "nginx":          ("🔀", "Configure Nginx as a reverse proxy for your Flask app on a VPS."),

    # Tools
    "git":            ("🌿", "Make sure every project is on GitHub with clear commits and a README."),
    "pytest":         ("✅", "Add unit tests to one of your Python projects using pytest — shows code quality."),
    "mlflow":         ("📦", "Add MLflow tracking to your ML project — logs metrics, params, and models."),
    "airflow":        ("💨", "Build a simple DAG in Apache Airflow for a data pipeline project."),
    "excel":          ("📗", "Learn VLOOKUP, pivot tables, and basic macros — still used everywhere."),
}

# Fallback tip for skills not in the dictionary
DEFAULT_TIP = ("💡", "Search for a beginner project using this skill on GitHub and build your own version.")


def get_skill_tips(missing_skills):
    """
    Takes a list of missing skill names and returns a list of dicts:
    [
        {
            "skill": "docker",
            "emoji": "🐳",
            "tip": "Dockerize one of your existing projects..."
        },
        ...
    ]
    """
    result = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        emoji, tip = SKILL_TIPS.get(skill_lower, DEFAULT_TIP)
        result.append({
            "skill": skill,
            "emoji": emoji,
            "tip": tip
        })
    return result