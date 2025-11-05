pipeline {
    agent { label 'mac' }

    environment {
        IMAGE_NAME = "fastapi-demo"
        CONTAINER_NAME = "fastapi-demo"
        API_PORT = "8000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning source repository"
                git branch: 'main', url: 'https://github.com/csabapatyi/devops-interview.git'
            }
        }

        stage('Python Linting') {
            steps {
                dir('fastapi-demo') {
                    echo "Running flake8 linting"
                    sh '''
                        python3 -m pip install --upgrade pip setuptools wheel
                        pip install flake8
                        echo "🔍 Running flake8 lint..."
                        flake8 --ignore=E501,W503,E203 .
                    '''
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                dir('fastapi-demo') {
                    echo "Running Bandit static analysis"
                    sh '''
                        pip install bandit
                        echo "🕵️♂️ Scanning for security issues..."
                        bandit -r app -ll -ii
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('fastapi-demo') {
                    echo "Building Docker image '${IMAGE_NAME}' using Podman"
                    sh 'podman build -t ${IMAGE_NAME}:latest .'
                }
            }
        }

        stage('Docker Image Scan') {
            steps {
                echo "Scanning Docker image for vulnerabilities (Trivy)"
                sh '''
                    if ! command -v trivy >/dev/null 2>&1; then
                        echo "Installing Trivy scanner..."
                        brew install trivy || \
                        curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
                    fi
                    echo "🔍 Running image scan..."
                    trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:latest || true
                '''
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Deploying ${IMAGE_NAME} container locally"
                sh '''
                    podman stop ${CONTAINER_NAME} || true
                    podman rm ${CONTAINER_NAME} || true
                    podman run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${API_PORT}:8000 \
                        ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                echo "Performing /health check"
                sh 'sleep 5 && curl -f http://localhost:${API_PORT}/health'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline finished successfully!"
        }
        failure {
            echo "❌ Pipeline failed."
        }
        always {
            echo "📋 Running cleanup summary"
            sh 'podman ps'
        }
    }
}