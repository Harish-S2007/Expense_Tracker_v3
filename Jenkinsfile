
pipeline {
    agent any

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
                echo 'V3 source code checked out.'
            }
        }

        stage('2. Check Tools') {
            steps {
                powershell '''
                    docker --version
                    kubectl version --client
                    python --version
                '''
            }
        }

        stage('3. Install Dependencies') {
            steps {
                powershell '''
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('4. Test Application') {
            steps {
                powershell '''
                    python -c "import app; print('V3 app imported successfully')"
                '''
            }
        }

        stage('5. Build Docker Image') {
            steps {
                powershell '''
                    docker build -t expense-tracker:v3 .
                '''
            }
        }

        stage('6. Deploy to Kubernetes') {
            steps {
                powershell '''
                    kubectl apply -f deployment.yaml
                    kubectl rollout status deployment/expense-v3 --timeout=180s
                '''
            }
        }

        stage('7. Verify Deployment') {
            steps {
                powershell '''
                    kubectl get deployment expense-v3
                    kubectl get pods -l app=expense-v3
                    kubectl get service expense-v3-service
                '''
            }
        }
    }
}
