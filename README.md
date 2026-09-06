# Employee History

A local-first employee/intern application portal built with Flask and SQLite.

## Features

- Two current openings: **AI / ML Engineer Intern** and **Marketing & Customer Handling**.
- Role details and responsibilities before applying.
- Personal, education, experience, skills, projects, career goals and availability fields.
- PDF, DOC and DOCX resume upload, maximum 5 MB.
- Unique Applicant ID for every submission.
- Local SQLite storage for applicant records.
- Local resume storage in `uploads/`.
- Password-protected local admin records view.

## Privacy

This repository is public source code. **Never commit applicant records, resumes, the SQLite database, `.env` files, or other personal information to GitHub.** The `.gitignore` file excludes local database and resume data.

## Windows setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:SECRET_KEY="replace-with-a-random-secret"
$env:ADMIN_PASSWORD="replace-with-a-strong-local-password"
python app.py
```

Open `http://127.0.0.1:5000`.

Admin: `http://127.0.0.1:5000/admin`

## macOS/Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="replace-with-a-random-secret"
export ADMIN_PASSWORD="replace-with-a-strong-local-password"
python app.py
```

Then open `http://127.0.0.1:5000`.

## Local data

- `data/employee_history.db` — applicant records
- `uploads/` — uploaded resumes

Both are intentionally excluded from GitHub.

## Structure

```text
employee-history/
├── app.py
├── database.py
├── roles.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── role.html
│   ├── application.html
│   ├── success.html
│   ├── admin_login.html
│   ├── admin.html
│   └── applicant.html
├── static/
│   └── style.css
├── data/                 # local only
└── uploads/              # local resumes only
```
