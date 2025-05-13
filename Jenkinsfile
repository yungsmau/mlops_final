pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        VENV_ACTIVATE = ".venv/bin/activate"

        DVC_ACCESS_KEY_ID = "urfu_mlops_admin"
        DVC_SECRET_ACCESS_KEY = "urfu_mlops_password"
        DVC_ENDPOINT_URL = 'http://51.250.94.139:9000'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    if (!fileExists(env.VENV_DIR)) {
                        echo "Creating virtual environment..."
                        sh """
                        python3 -m venv .venv
                        . ${VENV_ACTIVATE}
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        """
                    } else {
                        echo "Virtual environment already exists."
                    }

                }
            }
        }

        stage('Setup DVC and Pull Data') {
            steps {
                sh """
                . ${VENV_ACTIVATE}
                dvc remote modify myremote access_key_id ${DVC_ACCESS_KEY_ID}
                dvc remote modify myremote secret_access_key ${DVC_SECRET_ACCESS_KEY}
                dvc remote modify myremote endpointurl ${DVC_ENDPOINT_URL}
                dvc pull
                """
            }
        }

        stage('Train and Evaluate on Dirty Data') {
            steps {
                sh """
                . ${env.VENV_ACTIVATE}
                python pipeline/train.py --data data/dirty.csv --output model/model.joblib
                python pipeline/evaluate.py --model model/model.joblib --data data/dirty.csv --metrics pipeline/metrics.json
                """
            }
        }

        stage('Check Metrics and Retrain if Necessary') {
            steps {
                script {
                    // Запускаем тесты, проверяющие метрики
                    def testResult = sh(script: """
                        . ${env.VENV_ACTIVATE}
                        pytest --maxfail=1 --disable-warnings -q tests/test_metrics.py
                    """, returnStatus: true)

                    // Если тесты не прошли (возвращают ненулевой статус), перезапускаем обучение
                    if (testResult != 0) {
                        echo "Metrics failed the test, retraining on clean dataset..."
                        sh """
                        . ${env.VENV_ACTIVATE}
                        python pipeline/train.py --data data/clean.csv --output model/model.joblib
                        python pipeline/evaluate.py --model model/model.joblib --data data/clean.csv --metrics pipeline/metrics.json
                        """
                    } else {
                        echo "Model performance is acceptable."
                    }
                }
            }
        }

        stage('Build and Run Docker API') {
            steps {
                sh """
                docker build -t mymodel-api .
                docker run -d -p 8000:8000 mymodel-api
                """
            }
        }

    }
}