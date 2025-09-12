pipeline {
    agent any

    environment {
        IMAGE_NAME = "llama-fastapi"
        CONTAINER_NAME = "llama_api"
        MODEL_PATH = "/workspace/Llama-3-13b-hf"
        API_PORT = "11434"
    }

    stages {
        stage('Check NVIDIA Driver') {
            steps {
                script {
                    def status = sh(script: "command -v nvidia-smi", returnStatus: true)
                    if (status != 0) {
                        error "❌ NVIDIA driver not found on host. Install NVIDIA driver before proceeding."
                    }
                    sh "nvidia-smi"
                }
            }
        }

        stage('Check GPU Docker Support') {
            steps {
                script {
                    def gpuCheck = sh(script: "docker run --rm --gpus all nvidia/cuda:11.7.1-base-ubuntu22.04 nvidia-smi", returnStatus: true)
                    if (gpuCheck != 0) {
                        error "❌ Docker cannot access GPU. Install and configure NVIDIA Container Toolkit."
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME} .
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --gpus all \
                        --name ${CONTAINER_NAME} \
                        -p ${API_PORT}:${API_PORT} \
                        ${IMAGE_NAME}
                """
            }
        }

        stage('Download LLaMA Model') {
            steps {
                withCredentials([string(credentialsId: 'HF_TOKEN', variable: 'HF_TOKEN')]) {
                    sh """
                        docker exec -i ${CONTAINER_NAME} bash -c '
                            git lfs install
                            if [ ! -d "${MODEL_PATH}" ]; then
                                echo "Logging in to Hugging Face..."
                                huggingface-cli login --token $HF_TOKEN
                                echo "Cloning LLaMA model repository..."
                                GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/meta-llama/Llama-3-13b-hf ${MODEL_PATH}
                                cd ${MODEL_PATH} && git lfs pull
                            fi
                        '
                    """
                }
            }
        }

        stage('Test API') {
            steps {
                sh """
                    echo "Testing FastAPI endpoint..."
                    sleep 10
                    curl -f http://localhost:${API_PORT}/docs || (echo "API test failed" && exit 1)
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment succeeded!"
        }
        failure {
            echo "❌ Deployment failed. Check logs."
        }
    }
}
