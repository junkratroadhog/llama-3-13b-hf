pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'llama13-local:latest'
        DOCKER_CONTAINER = 'llama13-server'
        MODEL_PATH = '/workspace/Llama-3-13b-hf'
        API_PORT = '11434'
        GIT_REPO = 'https://github.com/junkratroadhog/llama-3-13b-hf.git'
        GIT_BRANCH = 'main'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${env.GIT_BRANCH}", url: "${env.GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'HF_TOKEN', variable: 'HF_TOKEN')]) {
                    sh """
                    docker build \
                        --build-arg MODEL_PATH=$MODEL_PATH \
                        --build-arg API_PORT=$API_PORT \
                        --build-arg HF_TOKEN=$HF_TOKEN \
                        -t $DOCKER_IMAGE .
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh """
                docker rm -f $DOCKER_CONTAINER || true
                docker run -d --gpus all -p $API_PORT:$API_PORT \
                    --name $DOCKER_CONTAINER $DOCKER_IMAGE
                """
            }
        }

        stage('Test API') {
            steps {
                sh """
                curl -X POST http://localhost:$API_PORT/generate \
                     -H "Content-Type: application/json" \
                     -d '{"prompt": "Write a Python function to reverse a string."}'
                """
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully!"
        }
        failure {
            echo "Deployment failed. Check logs."
        }
    }
}
