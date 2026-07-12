# 📄 AI Resume Analyzer

An NLP-powered resume analysis tool that scores resumes for ATS compatibility, matches them against a target job description, detects skill gaps across key technical domains, and recommends the best-fit career role — all from a single PDF upload.

**🔗 GitHub Repo:** [Kushal797-bit/ai-resume-analyzer](https://github.com/Kushal797-bit/ai-resume-analyzer)

---

## 📊 Overview

Most resume checkers stop at a keyword count. This tool goes further — it parses the raw PDF with NLP, extracts structured skills and sections, semantically compares the resume against a job description (not just keyword overlap), and generates a full analysis report: ATS score, JD match percentage, a 6-domain skill gap radar, ranked career recommendations, and a personalized, per-skill action plan to close the gaps — all downloadable as a PDF report.

---

## 🖼️ Screenshots

### Analysis Report Overview
At-a-glance summary: ATS score, JD match %, skills found, resume sections present, and the best-fit role match.

![AI Resume Analysis Report Overview](ai-resume-analyzer-screenshots/report-overview.png)

### ATS Score & Skill Gap Radar
A visual breakdown of resume strength across 6 key domains — Programming, Cloud/DevOps, ML/AI, Data, Backend, and AI Tools.

![ATS Score and Skill Gap Radar](ai-resume-analyzer-screenshots/ats-score-skill-radar.png)

### Job Description Match & Skill Comparison
Semantic JD match score, with matching and missing skills clearly separated so users know exactly what to add.

![JD Match and Skill Comparison](ai-resume-analyzer-screenshots/jd-match-skills.png)

### Personalized Tips & Resume Section Checklist
Actionable, per-skill improvement tips plus a recruiter-standard section checklist (Education, Experience, Projects, Skills, Certifications, Achievements, Summary).

![Improvement Tips and Section Checklist](ai-resume-analyzer-screenshots/improvement-tips-checklist.png)

---

## ✨ Features

- **ATS Score** — quantifies how well a resume is structured for applicant tracking systems
- **Job Description Match** — semantic similarity scoring between resume and JD (not just keyword overlap)
- **Skill Detection** — automatically identifies 40+ technical skills across programming languages, cloud/DevOps tools, ML/AI, and data
- **Skill Gap Radar** — visual coverage across 6 key domains: Programming, Cloud/DevOps, ML/AI, Data, Backend, AI Tools
- **Career Role Recommendations** — ranks the best-fit roles (e.g. DevOps Engineer, AI/ML Engineer, Backend Developer) by relevance score
- **Resume Section Checklist** — flags missing standard sections (e.g. Achievements) that recruiters expect to see
- **Personalized Improvement Tips** — one actionable step per missing skill
- **Downloadable PDF Report** — export the full analysis for offline review

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **NLP:** spaCy (resume parsing & entity extraction)
- **Semantic Matching:** Sentence Transformers (JD ↔ resume similarity)
- **Modeling:** Scikit-learn (role classification/recommendation)
- **Frontend:** HTML, CSS, Bootstrap

---

## 📁 Project Structure

```
ai-resume-analyzer/
├── dataset/                # Skills reference data / training data
├── static/                 # CSS and static assets
├── templates/               # HTML templates (Flask views, report page)
├── app.py                  # Flask application entry point
├── resume_parser.py        # PDF parsing & NLP extraction logic
├── skill_extractor.py      # Skill detection & matching logic
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### Run locally

```bash
# Clone the repo
git clone https://github.com/Kushal797-bit/ai-resume-analyzer.git
cd ai-resume-analyzer

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the app
python app.py
```

The app will be available at `http://localhost:5000`.

### Usage

1. Upload a resume in PDF format
2. (Optional) Paste in a target job description for JD match scoring
3. View the full analysis report — ATS score, skill gap radar, matching/missing skills, and role recommendations
4. Download the report as a PDF for offline reference

---

## 🔮 Future Improvements

- Deploy to a live, publicly hosted instance
- Support batch resume analysis (multiple resumes at once)
- Add support for `.docx` resumes in addition to PDF
- Expand the skill taxonomy with more role-specific keyword sets
- Add resume rewriting suggestions powered by an LLM

---

## 📬 Contact

**Kushal Upadhyay**
📧 kushalupadhyay06@gmail.com

If you find this project useful, consider giving it a ⭐!
