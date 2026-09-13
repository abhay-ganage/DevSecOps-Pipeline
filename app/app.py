
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "devsecops-codevault-secret"


# Large question bank
QUESTIONS = [
    {
        "question": "Which command shows running Docker containers?",
        "options": ["docker ps", "docker run", "docker images", "docker start"],
        "answer": "A",
    },
    {
        "question": "Which tool is commonly used for Infrastructure as Code?",
        "options": ["Terraform", "Git", "Jenkins", "Python"],
        "answer": "A",
    },
    {
        "question": "What does CI stand for in CI/CD?",
        "options": [
            "Code Integration",
            "Continuous Integration",
            "Cloud Integration",
            "Container Integration",
        ],
        "answer": "B",
    },
    {
        "question": "Which Python keyword is used to create a function?",
        "options": ["func", "def", "function", "create"],
        "answer": "B",
    },
    {
        "question": "Which Linux command displays the current directory?",
        "options": ["cd", "ls", "pwd", "dir"],
        "answer": "C",
    },
    {
        "question": "Which Dockerfile instruction specifies the base image?",
        "options": ["RUN", "CMD", "FROM", "BASE"],
        "answer": "C",
    },
    {
        "question": "Which command is used to build a Docker image?",
        "options": [
            "docker build",
            "docker create",
            "docker image-run",
            "docker compile",
        ],
        "answer": "A",
    },
    {
        "question": "Which command is used to download a Git repository?",
        "options": ["git pull", "git clone", "git fetch", "git download"],
        "answer": "B",
    },
    {
        "question": "Which file is commonly used to define a Jenkins pipeline?",
        "options": ["Jenkinsfile", "pipeline.yml", "jenkins.py", "build.xml"],
        "answer": "A",
    },
    {
        "question": "What does CD commonly mean in CI/CD?",
        "options": [
            "Code Development",
            "Continuous Deployment",
            "Container Development",
            "Cloud Distribution",
        ],
        "answer": "B",
    },
    {
        "question": "Which HTTP status code means 'Not Found'?",
        "options": ["200", "301", "404", "500"],
        "answer": "C",
    },
    {
        "question": "Which Python package is being used to create our web application?",
        "options": ["Django", "Flask", "NumPy", "Requests"],
        "answer": "B",
    },
    {
        "question": "Which command checks the installed Python version?",
        "options": ["python --version", "python --check", "python -info", "python version"],
        "answer": "A",
    },
    {
        "question": "Which Linux command lists files in a directory?",
        "options": ["pwd", "cd", "ls", "mkdir"],
        "answer": "C",
    },
    {
        "question": "What is the main purpose of a Docker container?",
        "options": [
            "Store passwords",
            "Package and run applications consistently",
            "Replace Git",
            "Create databases automatically",
        ],
        "answer": "B",
    },
    {
        "question": "Which Git command creates a new commit?",
        "options": ["git save", "git push", "git commit", "git upload"],
        "answer": "C",
    },
    {
        "question": "Which AWS service provides virtual servers?",
        "options": ["S3", "EC2", "RDS", "IAM"],
        "answer": "B",
    },
    {
        "question": "Which AWS service is primarily used for object storage?",
        "options": ["EC2", "RDS", "S3", "VPC"],
        "answer": "C",
    },
    {
        "question": "Which tool is commonly used to automate CI/CD pipelines?",
        "options": ["Jenkins", "MySQL", "Nginx", "PostgreSQL"],
        "answer": "A",
    },
    {
        "question": "Which Linux command creates a new directory?",
        "options": ["touch", "mkdir", "newdir", "createdir"],
        "answer": "B",
    },
    {
        "question": "What is the purpose of a .gitignore file?",
        "options": [
            "Delete the Git repository",
            "Specify files Git should ignore",
            "Create commits",
            "Configure Jenkins",
        ],
        "answer": "B",
    },
    {
        "question": "Which port is normally used by HTTP?",
        "options": ["21", "22", "80", "443"],
        "answer": "C",
    },
    {
        "question": "Which port is normally used by HTTPS?",
        "options": ["22", "53", "80", "443"],
        "answer": "D",
    },
    {
        "question": "Which protocol is commonly used for secure remote SSH access?",
        "options": ["FTP", "SSH", "HTTP", "SMTP"],
        "answer": "B",
    },
    {
        "question": "What is the purpose of unit tests?",
        "options": [
            "Build Docker images",
            "Test individual pieces of code",
            "Create AWS servers",
            "Push code to GitHub",
        ],
        "answer": "B",
    },
]


@app.route("/")
def index():
    # Start a completely new game
    session.clear()

    # Select 5 random questions from the full question bank
    selected_questions = random.sample(QUESTIONS, 5)

    session["questions"] = selected_questions
    session["current"] = 0
    session["score"] = 0
    session["lives"] = 3

    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    questions = session.get("questions")

    if not questions:
        return redirect(url_for("index"))

    current = session.get("current", 0)

    if request.method == "POST":
        selected = request.form.get("answer")
        question = questions[current]

        if selected == question["answer"]:
            session["score"] += 10
        else:
            session["lives"] -= 1

        # End game when:
        # 1. All questions are completed
        # 2. Player loses all lives
        if session["lives"] <= 0 or current >= len(questions) - 1:
            return redirect(url_for("result"))

        session["current"] += 1

    question = questions[session["current"]]

    return render_template(
        "game.html",
        question=question,
        level=session["current"] + 1,
        total=len(questions),
        score=session["score"],
        lives=session["lives"],
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    lives = session.get("lives", 0)

    total = len(session.get("questions", [])) * 10

    if score == total:
        message = "🔥 PERFECT SCORE! You're a DevOps Warrior!"
    elif score >= total * 0.6:
        message = "🚀 Great job! Keep improving your skills."
    else:
        message = "💡 Keep practicing. Every bug makes you better!"

    return render_template(
        "result.html",
        score=score,
        total=total,
        lives=lives,
        message=message,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

