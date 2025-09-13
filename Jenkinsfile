pipeline {
    agent any

    parameters {
        choice(name: 'MODE', choices: ['inference', 'training'], description: 'Run in inference (GGUF + llama.cpp) or training (HF + transformers)')
        string(name: 'MODEL_PATH', defaultValue: '/workspace/models/Llama-3-8B', description: 'Model storage path')
        string(name: 'HF_TOKEN', defaultValue: '', description: 'Hugging Face token (must have access to LLaMA models)')
    }

    environment {
        HF_HOME = "${WORKSPACE}/.cache/huggingface"
    }

    stages {

        stage('Setup Environment') {
            steps {
                sh '''
                  python3 -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                '''
            }
        }

        stage('Download Model') {
            steps {
                withEnv(["HF_TOKEN=${params.HF_TOKEN}", "MODEL_PATH=${params.MODEL_PATH}", "MODE=${params.MODE}"]) {
                    sh '''
                      chmod +x download_model.sh
                      ./download_model.sh
                    '''
                }
            }
        }

        stage('Build llama.cpp (Inference Only)') {
            when { expression { params.MODE == "inference" } }
            steps {
                sh '''
                  if [ ! -d llama.cpp ]; then
                    git clone https://github.com/ggerganov/llama.cpp
                  fi
                  cd llama.cpp
                  make
                '''
            }
        }

        stage('Run FastAPI Service') {
            steps {
                sh '''
                  . venv/bin/activate
                  if [ "${MODE}" = "inference" ]; then
                      # Run via llama.cpp (subprocess in app.py)
                      uvicorn app:app --host 0.0.0.0 --port 8000
                  else
                      # Run via Hugging Face transformers
                      uvicorn app:app --host 0.0.0.0 --port 8000
                  fi
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            echo "❌ Deployment failed. Check logs."
        }
    }
}
