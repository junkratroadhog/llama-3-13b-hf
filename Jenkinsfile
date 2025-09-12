pipeline {
    agent any

    environment {
        IMAGE_NAME = "llama-fastapi"
        CONTAINER_NAME = "llama_api"
        MODEL_PATH = "/workspace/Llama-3-13b-hf"
        API_PORT = "11434"
        NETWORK_NAME = "llama_network"
        VOLUME_NAME = "llama_volume"
    }

    stages {

        stage('Cleanup Existing Deployment') {
            steps {
                sh """
                    # Remove existing container if exists
                    if [ \$(docker ps -a -q -f name=${CONTAINER_NAME}) ]; then
                        echo "Removing existing container ${CONTAINER_NAME}..."
                        docker rm -f ${CONTAINER_NAME}
                    fi

                    # Remove Docker volume if exists
                    if [ \$(docker volume ls -q -f name=${VOLUME_NAME}) ]; then
                        echo "Removing existing volume ${VOLUME_NAME}..."
                        docker volume rm ${VOLUME_NAME}
                    fi

                    # Remove Docker network if exists
                    if [ \$(docker network ls -q -f name=${NETWORK_NAME}) ]; then
                        echo "Removing existing network ${NETWORK_NAME}..."
                        docker network rm ${NETWORK_NAME}
                    fi

                    # Recreate network and volume
                    docker network create ${NETWORK_NAME} || true
                    docker volume create ${VOLUME_NAME} || true
                """
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
                    docker run -d --gpus all \
                        --name ${CONTAINER_NAME} \
                        --network ${NETWORK_NAME} \
                        -v ${VOLUME_NAME}:${MODEL_PATH} \
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
                echo "Waiting for FastAPI endpoint..."
                for i in {1..30}; do
                    curl -f http://localhost:${API_PORT}/docs && break
                    echo "Waiting..."
                    sleep 2
                done
                curl -f http://localhost:${API_PORT}/docs || (echo "API test failed" && exit 1)
                """
            }
        }
    }
    
    post {
        cleanWs()
        success {
            echo "✅ Deployment succeeded!"
        }
        failure {
            echo "❌ Deployment failed. Check logs."
        }

    }
}
