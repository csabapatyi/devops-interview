pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-demo"
        CONTAINER_NAME = "fastapi-demo"
        API_PORT = "8000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning source repository"
                git branch: 'main', url: 'https://github.com/Tech-Modernization/devops-interview.git'
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
            sh 'podman ps'
        }
    }
}