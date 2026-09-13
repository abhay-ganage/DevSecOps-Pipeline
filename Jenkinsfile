
pipeline {
    agent any

    environment {
        DOCKER_PATH = 'C:\\Users\\Abhay\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
        TRIVY_PATH = 'C:\\Users\\Abhay\\AppData\\Local\\Microsoft\\WinGet\\Packages\\AquaSecurity.Trivy_Microsoft.Winget.Source_8wekyb3d8bbwe'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Setup') {
            steps {
                bat 'python --version'
                bat 'pip --version'
                bat 'pip install -r requirements.txt'
                bat 'pip install -r requirements-dev.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests'
            }
        }

        stage('Security Scan') {
            steps {
                bat 'bandit -r app'
                bat 'pip-audit -r requirements.txt'
            }
        }

        stage('Docker Build') {
            steps {
                bat '"%DOCKER_PATH%\\docker.exe" build -t codevault:1.0 .'
            }
        }

        stage('Tool Check') {
            steps {
                bat '"%DOCKER_PATH%\\docker.exe" --version'
                bat '"%TRIVY_PATH%\\trivy.exe" --version'
            }
        }

        stage('Trivy Scan') {
            steps {
                bat '"%TRIVY_PATH%\\trivy.exe" fs .'
            }
        }
    }

    post {
        success {
            echo 'CodeVault CI Pipeline completed successfully!'
        }

        failure {
            echo 'CodeVault CI Pipeline failed!'
        }
    }
}
