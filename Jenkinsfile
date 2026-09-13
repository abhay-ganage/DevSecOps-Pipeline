
pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Python 3.10.1\\python.exe'
        DOCKER_EXE = 'C:\\Users\\Abhay\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        TRIVY_EXE  = 'C:\\Users\\Abhay\\AppData\\Local\\Microsoft\\WinGet\\Links\\trivy.exe'

        IMAGE_NAME = 'codevault:1.0'
    }

    stages {

        stage('Python Setup') {
            steps {
                bat '''
                    echo ========================================
                    echo Checking Python
                    echo ========================================

                    if not exist "%PYTHON_EXE%" (
                        echo ERROR: Python was not found at:
                        echo %PYTHON_EXE%
                        exit /b 1
                    )

                    "%PYTHON_EXE%" --version
                    "%PYTHON_EXE%" -m pip --version

                    echo.
                    echo Installing application dependencies...
                    "%PYTHON_EXE%" -m pip install -r requirements.txt

                    if errorlevel 1 (
                        echo ERROR: Application dependency installation failed.
                        exit /b 1
                    )

                    echo.
                    echo Installing development dependencies...
                    "%PYTHON_EXE%" -m pip install -r requirements-dev.txt

                    if errorlevel 1 (
                        echo ERROR: Development dependency installation failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    echo ========================================
                    echo Running Tests
                    echo ========================================

                    "%PYTHON_EXE%" -m pytest tests

                    if errorlevel 1 (
                        echo ERROR: Tests failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Security Scan') {
            steps {
                bat '''
                    echo ========================================
                    echo Bandit Security Scan
                    echo ========================================

                    "%PYTHON_EXE%" -m bandit -r app

                    if errorlevel 1 (
                        echo ERROR: Bandit security scan failed.
                        exit /b 1
                    )

                    echo.
                    echo ========================================
                    echo pip-audit Dependency Scan
                    echo ========================================

                    "%PYTHON_EXE%" -m pip_audit -r requirements.txt

                    if errorlevel 1 (
                        echo ERROR: pip-audit found vulnerabilities.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Docker Build') {
            steps {
                bat '''
                    echo ========================================
                    echo Checking Docker
                    echo ========================================

                    if not exist "%DOCKER_EXE%" (
                        echo ERROR: Docker was not found at:
                        echo %DOCKER_EXE%
                        exit /b 1
                    )

                    "%DOCKER_EXE%" --version

                    echo.
                    echo ========================================
                    echo Building Docker Image
                    echo ========================================

                    "%DOCKER_EXE%" build -t %IMAGE_NAME% .

                    if errorlevel 1 (
                        echo ERROR: Docker build failed.
                        exit /b 1
                    )

                    echo.
                    echo Docker image built successfully:
                    echo %IMAGE_NAME%
                '''
            }
        }

        stage('Tool Check') {
            steps {
                bat '''
                    echo ========================================
                    echo Tool Check
                    echo ========================================

                    echo.
                    echo Python:
                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python check failed.
                        exit /b 1
                    )

                    echo.
                    echo Docker:
                    "%DOCKER_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Docker check failed.
                        exit /b 1
                    )

                    echo.
                    echo Trivy:
                    "%TRIVY_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Trivy check failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                bat '''
                    echo ========================================
                    echo Trivy Docker Image Scan
                    echo ========================================

                    if not exist "%TRIVY_EXE%" (
                        echo ERROR: Trivy was not found at:
                        echo %TRIVY_EXE%
                        exit /b 1
                    )

                    echo Using Trivy:
                    echo %TRIVY_EXE%

                    echo.
                    echo Scanning image:
                    echo %IMAGE_NAME%

                    "%TRIVY_EXE%" image --severity HIGH,CRITICAL %IMAGE_NAME%

                    if errorlevel 1 (
                        echo.
                        echo ERROR: Trivy found HIGH or CRITICAL vulnerabilities.
                        exit /b 1
                    )

                    echo.
                    echo Trivy scan completed successfully.
                '''
            }
        }
    }

    post {
        success {
            echo '========================================'
            echo 'CodeVault CI Pipeline SUCCESS!'
            echo '========================================'
        }

        failure {
            echo '========================================'
            echo 'CodeVault CI Pipeline FAILED!'
            echo '========================================'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}

