import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename

from resume_analyzer import analyze_resume
from resume_optimizer import extract_skills_from_job_description
from resume_generator import generate_resume_pdf


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
GENERATED_FOLDER = os.path.join(BASE_DIR, "generated_resumes")

ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

app.secret_key = "ai_resume_project_secret_key_2026"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():

    if request.method == "POST":

        if "resume" not in request.files:
            flash("Please upload a resume PDF.")
            return redirect(request.url)

        resume_file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()

        if resume_file.filename == "":
            flash("Please select a resume PDF.")
            return redirect(request.url)

        if not job_description:
            flash("Please enter the job description.")
            return redirect(request.url)

        if not allowed_file(resume_file.filename):
            flash("Only PDF files are allowed.")
            return redirect(request.url)

        original_filename = secure_filename(resume_file.filename)

        unique_filename = (
            f"{uuid.uuid4().hex}_{original_filename}"
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_filename
        )

        resume_file.save(file_path)

        try:
            result = analyze_resume(
                file_path,
                job_description
            )

            return render_template(
                "analysis_result.html",
                result=result
            )

        except Exception as error:
            flash(f"Error while analyzing resume: {str(error)}")
            return redirect(url_for("analyzer"))

    return render_template("analyzer.html")


@app.route("/optimizer", methods=["GET", "POST"])
def optimizer():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        linkedin = request.form.get("linkedin", "").strip()
        github = request.form.get("github", "").strip()
        location = request.form.get("location", "").strip()

        education = request.form.get("education", "").strip()
        projects = request.form.get("projects", "").strip()
        experience = request.form.get("experience", "").strip()
        achievements = request.form.get("achievements", "").strip()

        existing_skills = request.form.get(
            "existing_skills",
            ""
        ).strip()

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        if not name or not email or not job_description:
            flash(
                "Name, email and job description are required."
            )
            return redirect(request.url)

        detected_skills = extract_skills_from_job_description(
            job_description
        )

        if existing_skills:
            user_skills = [
                skill.strip()
                for skill in existing_skills.split(",")
                if skill.strip()
            ]
        else:
            user_skills = []

        final_skills = []

        for skill in user_skills + detected_skills:
            if skill.lower() not in [
                item.lower()
                for item in final_skills
            ]:
                final_skills.append(skill)

        resume_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "location": location,
            "education": education,
            "projects": projects,
            "experience": experience,
            "achievements": achievements,
            "skills": final_skills,
            "detected_skills": detected_skills,
            "job_description": job_description
        }

        return render_template(
            "optimized_resume.html",
            resume=resume_data
        )

    return render_template("optimizer.html")


@app.route("/download_resume", methods=["POST"])
def download_resume():

    resume_data = {
        "name": request.form.get("name", ""),
        "email": request.form.get("email", ""),
        "phone": request.form.get("phone", ""),
        "linkedin": request.form.get("linkedin", ""),
        "github": request.form.get("github", ""),
        "location": request.form.get("location", ""),
        "education": request.form.get("education", ""),
        "projects": request.form.get("projects", ""),
        "experience": request.form.get("experience", ""),
        "achievements": request.form.get("achievements", ""),
        "skills": request.form.getlist("skills")
    }

    safe_name = secure_filename(
        resume_data["name"].replace(" ", "_")
    )

    if not safe_name:
        safe_name = "resume"

    filename = f"{safe_name}_Resume.pdf"

    output_path = os.path.join(
        app.config["GENERATED_FOLDER"],
        filename
    )

    generate_resume_pdf(
        resume_data,
        output_path
    )

    return send_file(
        output_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large. Maximum allowed size is 10 MB.")
    return redirect(request.url)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )