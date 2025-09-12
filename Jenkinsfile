pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'llama13-local:latest'
        DOCKER_CONTAINER = 'llama13-server'
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
                sh """
                docker build \
                    --build-arg API_PORT=$API_PORT \
                    -t $DOCKER_IMAGE .
                """
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
}
