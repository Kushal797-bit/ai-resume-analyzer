import joblib


clf = joblib.load("ml/models/role_classifier.pkl")
vectorizer = joblib.load("ml/models/tfidf_vectorizer.pkl")

def predict_role(resume_text):
    resume_vec = vectorizer.transform([resume_text])
    prediction = clf.predict(resume_vec)
    return prediction[0]

from ml.match_score import get_match_score
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills, predict_job_role, calculate_ats_score, find_missing_skills, get_top_roles, detect_resume_sections, calculate_radar_scores,check_resume_length,get_skill_tips

from flask import Flask, render_template, request, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import traceback
from datetime import datetime

app = Flask(__name__)
app.secret_key = "resume-analyzer-secret-2024"


with open("dataset/skills.txt", "r") as file:
    skills_list = [skill.strip() for skill in file.readlines() if skill.strip()]


job_roles = {
    "Data Scientist": {
        "python": 5, "pandas": 5, "numpy": 5,
        "machine learning": 10, "matplotlib": 4,
        "seaborn": 4, "sql": 6, "data science": 10
    },
    "AI/ML Engineer": {
        "python": 6, "machine learning": 10, "deep learning": 10,
        "tensorflow": 9, "pytorch": 9, "nlp": 8,
        "flask": 5, "docker": 5
    },
    "Data Analyst": {
        "sql": 10, "excel": 8, "power bi": 9, "tableau": 9,
        "python": 5, "pandas": 5, "data visualization": 8
    },
    "Backend Developer": {
        "python": 8, "flask": 9, "django": 9, "rest api": 9,
        "mysql": 7, "mongodb": 7, "git": 5, "docker": 5
    },
    "DevOps Engineer": {
        "docker": 10, "aws": 10, "ci/cd": 10, "nginx": 8,
        "prometheus": 8, "grafana": 8, "github actions": 9,
        "git": 5, "linux": 7, "kubernetes": 10
    }
}

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




def draw_section_heading(c, y, width, title):
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.rect(40, y - 6, width - 80, 22, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, title)
    return y - 30


def draw_ats_bar(c, y, width, score):
    bar_x, bar_width, bar_height = 50, width - 100, 16
    c.setFillColor(colors.HexColor("#E0E0E0"))
    c.roundRect(bar_x, y, bar_width, bar_height, 4, fill=True, stroke=False)
    fill_color = (
        colors.HexColor("#27AE60") if score >= 80
        else colors.HexColor("#F39C12") if score >= 50
        else colors.HexColor("#E74C3C")
    )
    filled_width = (score / 100) * bar_width
    c.setFillColor(fill_color)
    c.roundRect(bar_x, y, filled_width, bar_height, 4, fill=True, stroke=False)
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(bar_x + filled_width + 6, y + 3, f"{score}%")
    return y - 30


def draw_skill_badges(c, y, width, skill_list, badge_color, text_color):
    x, max_x = 50, width - 50
    c.setFont("Helvetica", 9)
    for skill in skill_list:
        skill_width = c.stringWidth(skill, "Helvetica", 9) + 16
        if x + skill_width > max_x:
            x = 50
            y -= 20
        c.setFillColor(colors.HexColor(badge_color))
        c.roundRect(x, y - 4, skill_width, 16, 4, fill=True, stroke=False)
        c.setFillColor(colors.HexColor(text_color))
        c.drawString(x + 8, y + 1, skill)
        x += skill_width + 8
    return y - 24



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if not file or file.filename == "":
        return render_template("index.html", error="Please select a PDF file to upload.")
    if not allowed_file(file.filename):
        return render_template("index.html", error="Only PDF files are allowed.")
    if not job_description:
        return render_template("index.html", error="Please paste a job description.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        resume_text = extract_text_from_pdf(filepath)
        predicted_role = predict_role(resume_text)
        print("ML Predicted Role:", predicted_role)

        if not resume_text.strip():
            return render_template("index.html", error="Could not read text from your PDF. Make sure it is not a scanned image.")

        
        skills        = extract_skills(resume_text, skills_list)
        jd_skills     = extract_skills(job_description, skills_list)

        matching_skills = list(set(skills) & set(jd_skills))

        jd_match_score = get_match_score(
        resume_text,
        job_description
         )
        print("Semantic JD Match Score:", jd_match_score)
        missing_jd_skills = list(set(jd_skills) - set(skills))


    role_mapping = {
    "Data Science": "Data Scientist",
    "Machine Learning": "AI/ML Engineer",
    "Python Developer": "Backend Developer"
}

    predicted_role = role_mapping.get(predicted_role, predicted_role)


    if predicted_role not in job_roles:
       predicted_role = "Data Scientist"

       
        

        required_skills = job_roles[predicted_role]
        ats_score        = calculate_ats_score(skills, required_skills)
        missing_skills   = find_missing_skills(skills, required_skills)
        skill_tips = get_skill_tips(missing_skills)
        top_roles        = get_top_roles(skills, job_roles)
        section_report   = detect_resume_sections(resume_text)
        radar_scores = calculate_radar_scores(skills)
        length_report    = check_resume_length(resume_text)   

        
        session["skills"]         = skills
        session["predicted_role"] = predicted_role
        session["ats_score"]      = ats_score
        session["missing_skills"] = missing_skills
        session["jd_match_score"] = jd_match_score
        session["top_roles"]      = top_roles

        return render_template(
            "result.html",
            skills=skills,
            predicted_role=predicted_role,
            ats_score=ats_score,
            missing_skills=missing_skills,
            top_roles=top_roles,
            jd_match_score=jd_match_score,
            matching_skills=matching_skills,
            missing_jd_skills=missing_jd_skills,
            section_report=section_report,
            length_report=length_report, 
            radar_scores=radar_scores,  
            skill_tips=skill_tips,          
        )

    
except Exception as e:
    traceback.print_exc()
    print(e)
    return render_template(
        "index.html",
        error=f"An error occurred while analyzing your resume: {str(e)}"
    )


@app.route("/download-report")
def download_report():
    skills         = session.get("skills", [])
    predicted_role = session.get("predicted_role")
    ats_score      = session.get("ats_score", 0)
    missing_skills = session.get("missing_skills", [])
    jd_match_score = session.get("jd_match_score", 0)
    top_roles      = session.get("top_roles", [])

    if not predicted_role:
        return redirect(url_for("home"))

    pdf_path = os.path.join("uploads", "resume_report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height

    # Header
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.rect(0, height - 70, width, 70, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 40, "AI Resume Analysis Report")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 58, f"Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    y = height - 90

    
    y = draw_section_heading(c, y, width, "BEST MATCHING ROLE")
    c.setFillColor(colors.HexColor("#2980B9"))
    c.roundRect(50, y - 4, 200, 22, 6, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(58, y + 3, predicted_role)
    y -= 36

    # ATS Score
    y = draw_section_heading(c, y, width, "ATS SCORE")
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "How well your resume matches the predicted role:")
    y -= 18
    y = draw_ats_bar(c, y, width, ats_score)

    # JD Match
    y = draw_section_heading(c, y, width, "JOB DESCRIPTION MATCH SCORE")
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "How well your resume matches the pasted job description:")
    y -= 18
    y = draw_ats_bar(c, y, width, jd_match_score)

    
    y = draw_section_heading(c, y, width, "TOP CAREER RECOMMENDATIONS")
    for i, (role, score) in enumerate(top_roles, start=1):
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{i}.  {role}")
        c.setFont("Helvetica", 10)
        c.drawString(200, y, f"(Match score: {score})")
        y -= 18
    y -= 8

    # Detected Skills
    y = draw_section_heading(c, y, width, "DETECTED SKILLS")
    if skills:
        y = draw_skill_badges(c, y, width, skills, "#D5E8D4", "#27AE60")
    else:
        c.setFillColor(colors.HexColor("#999999"))
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "No skills detected.")
        y -= 20
    y -= 8

    
    y = draw_section_heading(c, y, width, "MISSING SKILLS  (add these to improve your score)")
    if missing_skills:
        y = draw_skill_badges(c, y, width, missing_skills, "#F8D7DA", "#E74C3C")
    else:
        c.setFillColor(colors.HexColor("#27AE60"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Great! No missing skills for this role.")
        y -= 20

    
    c.setFillColor(colors.HexColor("#BDC3C7"))
    c.rect(0, 0, width, 30, fill=True, stroke=False)
    c.setFillColor(colors.HexColor("#7F8C8D"))
    c.setFont("Helvetica", 8)
    c.drawString(40, 10, "Generated by AI Resume Analyzer  •  For personal use only")
    c.drawRightString(width - 40, 10, "Page 1")

    c.save()
    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)