import os
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-secret")


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

    # =========================
    # Additional 50 Questions
    # =========================

    {
        "question": "What does DevOps primarily aim to improve?",
        "options": [
            "Only software design",
            "Collaboration between development and operations",
            "Only database performance",
            "Only frontend development",
        ],
        "answer": "B",
    },
    {
        "question": "Which Git command uploads local commits to a remote repository?",
        "options": ["git push", "git upload", "git send", "git commit"],
        "answer": "A",
    },
    {
        "question": "Which Git command downloads changes from a remote repository and merges them?",
        "options": ["git clone", "git pull", "git push", "git merge-only"],
        "answer": "B",
    },
    {
        "question": "Which Git command displays the current repository status?",
        "options": ["git check", "git status", "git state", "git info"],
        "answer": "B",
    },
    {
        "question": "Which command creates a new Git branch?",
        "options": ["git branch", "git new", "git create-branch", "git make"],
        "answer": "A",
    },
    {
        "question": "Which command switches to another Git branch?",
        "options": ["git move", "git switch", "git change", "git branch-go"],
        "answer": "B",
    },
    {
        "question": "What is a Docker image?",
        "options": [
            "A running process",
            "A template used to create containers",
            "A Git repository",
            "A virtual machine",
        ],
        "answer": "B",
    },
    {
        "question": "Which Docker command downloads an image from a registry?",
        "options": ["docker fetch", "docker pull", "docker download", "docker get"],
        "answer": "B",
    },
    {
        "question": "Which Docker command starts a new container?",
        "options": ["docker run", "docker start-new", "docker launch", "docker execute"],
        "answer": "A",
    },
    {
        "question": "Which Docker command lists available images?",
        "options": ["docker ps", "docker images", "docker list-images", "docker show"],
        "answer": "B",
    },
    {
        "question": "Which Dockerfile instruction executes commands while building an image?",
        "options": ["RUN", "START", "EXEC", "COMMAND"],
        "answer": "A",
    },
    {
        "question": "Which Dockerfile instruction defines the default command for a container?",
        "options": ["RUN", "CMD", "EXECUTE", "START"],
        "answer": "B",
    },
    {
        "question": "Which command stops a running Docker container?",
        "options": ["docker pause", "docker stop", "docker kill-all", "docker shutdown"],
        "answer": "B",
    },
    {
        "question": "Which command removes a Docker container?",
        "options": ["docker delete", "docker rm", "docker remove-container", "docker erase"],
        "answer": "B",
    },
    {
        "question": "What is Docker Compose mainly used for?",
        "options": [
            "Managing multiple containerized services",
            "Writing Python code",
            "Managing Git branches",
            "Creating AWS accounts",
        ],
        "answer": "A",
    },
    {
        "question": "Which command is commonly used to start services defined in Docker Compose?",
        "options": [
            "docker compose up",
            "docker compose start-all-code",
            "docker compose launch",
            "docker compose run-server",
        ],
        "answer": "A",
    },
    {
        "question": "What does Kubernetes primarily manage?",
        "options": [
            "Source code",
            "Containerized applications",
            "Git repositories",
            "SQL queries",
        ],
        "answer": "B",
    },
    {
        "question": "Which command-line tool is commonly used to interact with Kubernetes?",
        "options": ["kubectl", "kubecli", "k8sctl", "kubecommand"],
        "answer": "A",
    },
    {
        "question": "Which Kubernetes object is used to run one or more containers?",
        "options": ["Pod", "Bucket", "Image", "VolumeFile"],
        "answer": "A",
    },
    {
        "question": "Which Kubernetes object provides a stable network endpoint for Pods?",
        "options": ["Service", "DeploymentFile", "NodePortOnly", "ConfigMap"],
        "answer": "A",
    },
    {
        "question": "Which Kubernetes object manages replicated Pods?",
        "options": ["Deployment", "Secret", "ServiceAccount", "ConfigMap"],
        "answer": "A",
    },
    {
        "question": "Which command lists Kubernetes Pods?",
        "options": ["kubectl get pods", "kubectl list pods", "kubectl show pods", "kubectl pods"],
        "answer": "A",
    },
    {
        "question": "Which AWS service provides managed relational databases?",
        "options": ["S3", "RDS", "EC2", "CloudFront"],
        "answer": "B",
    },
    {
        "question": "What is AWS IAM used for?",
        "options": [
            "Managing identities and permissions",
            "Creating Docker images",
            "Running Python scripts",
            "Managing Git commits",
        ],
        "answer": "A",
    },
    {
        "question": "What does AWS VPC stand for?",
        "options": [
            "Virtual Private Cloud",
            "Virtual Public Container",
            "Virtual Processing Center",
            "Virtual Platform Cloud",
        ],
        "answer": "A",
    },
    {
        "question": "Which AWS service is commonly used for monitoring resources and applications?",
        "options": ["CloudWatch", "CloudTrailDNS", "Route53", "S3"],
        "answer": "A",
    },
    {
        "question": "Which AWS service provides DNS management?",
        "options": ["Route 53", "EC2", "IAM", "SQS"],
        "answer": "A",
    },
    {
        "question": "What is an AWS Security Group?",
        "options": [
            "A virtual firewall for AWS resources",
            "A Git repository",
            "A Docker image",
            "A database",
        ],
        "answer": "A",
    },
    {
        "question": "Which AWS service can distribute traffic across multiple targets?",
        "options": [
            "Elastic Load Balancing",
            "S3",
            "IAM",
            "CloudTrail",
        ],
        "answer": "A",
    },
    {
        "question": "What is an EC2 instance?",
        "options": [
            "A virtual server",
            "An object storage bucket",
            "A database table",
            "A Git branch",
        ],
        "answer": "A",
    },
    {
        "question": "What does DNS stand for?",
        "options": [
            "Domain Name System",
            "Digital Network Service",
            "Domain Network Security",
            "Dynamic Name Server",
        ],
        "answer": "A",
    },
    {
        "question": "What is the main purpose of DNS?",
        "options": [
            "Translate domain names to IP addresses",
            "Encrypt passwords",
            "Build Docker images",
            "Run Jenkins pipelines",
        ],
        "answer": "A",
    },
    {
        "question": "Which protocol is connection-oriented?",
        "options": ["TCP", "UDP", "HTTP", "DNS"],
        "answer": "A",
    },
    {
        "question": "Which protocol is generally connectionless?",
        "options": ["TCP", "UDP", "SSH", "HTTPS"],
        "answer": "B",
    },
    {
        "question": "What does IP stand for in networking?",
        "options": [
            "Internet Protocol",
            "Internal Port",
            "Internet Process",
            "Integrated Protocol",
        ],
        "answer": "A",
    },
    {
        "question": "Which command tests network connectivity to a host?",
        "options": ["ping", "connect", "nettest", "hostcheck"],
        "answer": "A",
    },
    {
        "question": "Which Linux command displays running processes?",
        "options": ["ps", "proc", "run", "process-list"],
        "answer": "A",
    },
    {
        "question": "Which Linux command is commonly used to change file permissions?",
        "options": ["chmod", "chperm", "permission", "modfile"],
        "answer": "A",
    },
    {
        "question": "Which Linux command changes the owner of a file?",
        "options": ["chown", "owner", "chmod", "chuser"],
        "answer": "A",
    },
    {
        "question": "Which Linux command is commonly used to create an empty file?",
        "options": ["touch", "mkfile", "create", "new"],
        "answer": "A",
    },
    {
        "question": "Which Linux command removes a file?",
        "options": ["rm", "delete", "remove-file", "erase"],
        "answer": "A",
    },
    {
        "question": "What is Terraform state used for?",
        "options": [
            "Tracking infrastructure managed by Terraform",
            "Storing Docker images",
            "Running Jenkins",
            "Managing Python packages",
        ],
        "answer": "A",
    },
    {
        "question": "Which Terraform command initializes a working directory?",
        "options": [
            "terraform init",
            "terraform start",
            "terraform setup",
            "terraform create",
        ],
        "answer": "A",
    },
    {
        "question": "Which Terraform command previews infrastructure changes?",
        "options": [
            "terraform plan",
            "terraform preview",
            "terraform check",
            "terraform inspect",
        ],
        "answer": "A",
    },
    {
        "question": "Which Terraform command applies infrastructure changes?",
        "options": [
            "terraform apply",
            "terraform deploy",
            "terraform start",
            "terraform execute",
        ],
        "answer": "A",
    },
    {
        "question": "What is Jenkins mainly used for?",
        "options": [
            "Automating software delivery pipelines",
            "Object storage",
            "Database management",
            "DNS resolution",
        ],
        "answer": "A",
    },
    {
        "question": "What is the purpose of a Jenkins stage?",
        "options": [
            "Organize pipeline steps",
            "Store Docker images",
            "Create Git repositories",
            "Replace Python",
        ],
        "answer": "A",
    },
    {
        "question": "What does SAST generally mean?",
        "options": [
            "Static Application Security Testing",
            "Secure Application Server Technology",
            "System Application Security Tool",
            "Static AWS Security Testing",
        ],
        "answer": "A",
    },
    {
        "question": "What is Bandit commonly used for in Python projects?",
        "options": [
            "Finding common security issues in Python code",
            "Building Docker images",
            "Managing AWS EC2 instances",
            "Running Kubernetes clusters",
        ],
        "answer": "A",
    },
    {
        "question": "What is Trivy commonly used for?",
        "options": [
            "Scanning containers and other artifacts for vulnerabilities",
            "Writing Python code",
            "Creating Git branches",
            "Managing DNS",
        ],
        "answer": "A",
    },
    {
        "question": "What is the purpose of pip-audit?",
        "options": [
            "Check Python dependencies for known vulnerabilities",
            "Build Docker containers",
            "Deploy Kubernetes Pods",
            "Manage Git history",
        ],
        "answer": "A",
    },
    {
        "question": "What does HTTP status code 200 normally indicate?",
        "options": [
            "Successful request",
            "Not Found",
            "Server Error",
            "Unauthorized",
        ],
        "answer": "A",
    },
    {
        "question": "What does HTTP status code 500 normally indicate?",
        "options": [
            "Internal Server Error",
            "Successful Request",
            "Not Found",
            "Moved Permanently",
        ],
        "answer": "A",
    },
    {
        "question": "What is HTTPS primarily used for?",
        "options": [
            "Secure communication over HTTP",
            "File compression",
            "Database backup",
            "Container orchestration",
        ],
        "answer": "A",
    },
    {
        "question": "Which Python data type stores key-value pairs?",
        "options": ["Dictionary", "List", "Tuple", "String"],
        "answer": "A",
    },
    {
        "question": "Which Python data type is ordered and mutable?",
        "options": ["List", "Tuple", "String", "Integer"],
        "answer": "A",
    },
    {
        "question": "Which Python function returns the number of items in a collection?",
        "options": ["len()", "count()", "size()", "length()"],
        "answer": "A",
    },
]


@app.route("/")
def index():
    # Start a completely new game
    session.clear()

    # Select 5 random questions from the full question bank
    selected_questions = random.sample(QUESTIONS, 5)  # nosec B311

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
    app.run(host="0.0.0.0", port=5000, debug=False)  # nosec B104