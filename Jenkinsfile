pipeline {
    agent any

    environment {
        PYTHON_HOME = 'C:\\Python 3.10.1'
        TRIVY_HOME = 'C:\\Users\\Abhay\\AppData\\Local\\Microsoft\\WinGet\\Packages\\AquaSecurity.Trivy_Microsoft.Winget.Source_8wekyb3d8bbwe'
        PATH = "${PYTHON_HOME};${PYTHON_HOME}\\Scripts;${TRIVY_HOME};${env.PATH}"
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
                bat 'docker build -t codevault:1.0 .'
            }
        }

        stage('Tool Check') {
            steps {
                bat 'where python'
                bat 'python --version'
                bat 'where docker'
                bat 'docker --version'
                bat 'where trivy'
                bat 'trivy --version'
            }
        }

        stage('Trivy Scan') {
            steps {
                bat 'trivy fs .'
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