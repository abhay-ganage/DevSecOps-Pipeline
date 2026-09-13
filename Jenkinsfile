
pipeline {
    agent any

    environment {
        IMAGE_NAME = "codevault"
        IMAGE_TAG  = "1.0"

        // Docker Desktop path for Jenkins Windows service
        DOCKER_PATH = "C:\\Program Files\\Docker\\Docker\\resources\\bin"

        // Common Trivy installation paths
        TRIVY_PATH_1 = "C:\\Program Files\\trivy"
        TRIVY_PATH_2 = "C:\\ProgramData\\chocolatey\\bin"
        TRIVY_PATH_3 = "C:\\Program Files\\Trivy"

        // Add Docker and possible Trivy locations to PATH
        PATH = "${DOCKER_PATH};${TRIVY_PATH_1};${TRIVY_PATH_2};${TRIVY_PATH_3};${env.PATH}"
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
                bat 'docker --version'
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Tool Check') {
            steps {
                echo 'Checking installed DevSecOps tools...'

                // Do NOT use "where docker" because Jenkins
                // does not have the Windows where command in PATH.
                bat 'docker --version'

                // Check Trivy
                bat '''
                    if exist "C:\\Program Files\\trivy\\trivy.exe" (
                        echo Trivy found in C:\\Program Files\\trivy
                        "C:\\Program Files\\trivy\\trivy.exe" --version
                    ) else if exist "C:\\ProgramData\\chocolatey\\bin\\trivy.exe" (
                        echo Trivy found in Chocolatey
                        "C:\\ProgramData\\chocolatey\\bin\\trivy.exe" --version
                    ) else if exist "C:\\Program Files\\Trivy\\trivy.exe" (
                        echo Trivy found in C:\\Program Files\\Trivy
                        "C:\\Program Files\\Trivy\\trivy.exe" --version
                    ) else (
                        echo ERROR: Trivy executable was not found.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                bat '''
                    if exist "C:\\Program Files\\trivy\\trivy.exe" (
                        "C:\\Program Files\\trivy\\trivy.exe" image --severity HIGH,CRITICAL codevault:1.0
                    ) else if exist "C:\\ProgramData\\chocolatey\\bin\\trivy.exe" (
                        "C:\\ProgramData\\chocolatey\\bin\\trivy.exe" image --severity HIGH,CRITICAL codevault:1.0
                    ) else if exist "C:\\Program Files\\Trivy\\trivy.exe" (
                        "C:\\Program Files\\Trivy\\trivy.exe" image --severity HIGH,CRITICAL codevault:1.0
                    ) else (
                        echo ERROR: Trivy executable was not found.
                        exit /b 1
                    )
                '''
            }
        }
    }

    post {
        success {
            echo 'CodeVault CI Pipeline completed successfully!'
            echo 'Tests passed.'
            echo 'Security scans passed.'
            echo 'Docker image built successfully.'
            echo 'Trivy scan completed.'
        }

        failure {
            echo 'CodeVault CI Pipeline failed!'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}

