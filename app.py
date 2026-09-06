from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from database import init_db, save_application, list_applications, get_application
from roles import ROLES
from pathlib import Path
from datetime import datetime
import os
import uuid

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-dev-change-me")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

init_db()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def applicant_id() -> str:
    return f"EMP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


@app.route("/")
def home():
    return render_template("home.html", roles=ROLES)


@app.route("/role/<role_id>")
def role(role_id):
    role_data = ROLES.get(role_id)
    if not role_data:
        abort(404)
    return render_template("role.html", role=role_data, role_id=role_id)


@app.route("/apply/<role_id>", methods=["GET", "POST"])
def apply(role_id):
    role_data = ROLES.get(role_id)
    if not role_data:
        abort(404)

    if request.method == "GET":
        return render_template("application.html", role=role_data, role_id=role_id)

    form = request.form
    required = ["full_name", "email", "phone", "city", "highest_qualification", "institution", "graduation_year"]
    if any(not form.get(field, "").strip() for field in required):
        flash("Please complete all required fields.", "error")
        return render_template("application.html", role=role_data, role_id=role_id, form=form)

    resume = request.files.get("resume")
    if not resume or not resume.filename:
        flash("Please upload your resume.", "error")
        return render_template("application.html", role=role_data, role_id=role_id, form=form)
    if not allowed_file(resume.filename):
        flash("Resume must be PDF, DOC, or DOCX.", "error")
        return render_template("application.html", role=role_data, role_id=role_id, form=form)

    record_id = applicant_id()
    safe_name = secure_filename(resume.filename)
    stored_name = f"{record_id}_{safe_name}"
    resume.save(UPLOAD_DIR / stored_name)

    data = {
        "applicant_id": record_id,
        "role_id": role_id,
        "role_title": role_data["title"],
        "full_name": form["full_name"].strip(),
        "email": form["email"].strip(),
        "phone": form["phone"].strip(),
        "city": form["city"].strip(),
        "linkedin": form.get("linkedin", "").strip(),
        "highest_qualification": form["highest_qualification"].strip(),
        "institution": form["institution"].strip(),
        "graduation_year": form["graduation_year"].strip(),
        "education_details": form.get("education_details", "").strip(),
        "experience": form.get("experience", "").strip(),
        "skills": form.get("skills", "").strip(),
        "projects": form.get("projects", "").strip(),
        "career_goals": form.get("career_goals", "").strip(),
        "availability": form.get("availability", "").strip(),
        "resume_filename": safe_name,
        "resume_path": stored_name,
        "consent": 1 if form.get("consent") else 0,
    }
    save_application(data)
    return render_template("success.html", data=data)


@app.route("/admin")
def admin():
    expected = os.environ.get("ADMIN_PASSWORD", "admin123")
    if request.args.get("password") != expected:
        return render_template("admin_login.html"), 401
    applications = list_applications()
    return render_template("admin.html", applications=applications)


@app.route("/admin/applicant/<applicant_id>")
def applicant_detail(applicant_id):
    expected = os.environ.get("ADMIN_PASSWORD", "admin123")
    if request.args.get("password") != expected:
        return render_template("admin_login.html"), 401
    data = get_application(applicant_id)
    if not data:
        abort(404)
    return render_template("applicant.html", data=data, password=expected)


@app.route("/uploads/<path:filename>")
def download_resume(filename):
    expected = os.environ.get("ADMIN_PASSWORD", "admin123")
    if request.args.get("password") != expected:
        abort(401)
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


@app.errorhandler(413)
def too_large(_error):
    return "Resume is too large. Maximum allowed size is 5 MB.", 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
