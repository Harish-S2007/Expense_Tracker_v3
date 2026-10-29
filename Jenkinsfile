
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\hp\\expense_tracker_v3\\.venv\\Scripts\\python.exe'
        DOCKER = 'C:\\Users\\hp\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        KUBECTL = 'C:\\Users\\hp\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\kubectl.exe'
        KUBECONFIG = 'C:\\Users\\hp\\.kube\\config'
        IMAGE_NAME = 'expense-tracker:v3'
    }

    stages {

        stage('1. Checkout') {
            steps {
                checkout scm
                echo 'V3 source code checked out successfully.'
            }
        }

        stage('2. Check Tools') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    & $env:DOCKER --version
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker is not available."
                    }

                    & $env:KUBECTL version --client
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubectl is not available."
                    }

                    python --version
                    if ($LASTEXITCODE -ne 0) {
                        throw "Python is not available."
                    }
                '''
            }
        }

        stage('3. Install Dependencies') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    python -m pip install -r requirements.txt
                    if ($LASTEXITCODE -ne 0) {
                        throw "Dependency installation failed."
                    }
                '''
            }
        }

        stage('4. Test Application') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    python -c "import app; print('V3 application imported successfully')"
                    if ($LASTEXITCODE -ne 0) {
                        throw "Application test failed."
                    }
                '''
            }
        }

        stage('5. Build Docker Image') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    & $env:DOCKER build -t $env:IMAGE_NAME .
                    if ($LASTEXITCODE -ne 0) {
                        throw "Docker image build failed."
                    }

                    & $env:DOCKER images $env:IMAGE_NAME
                '''
            }
        }

        stage('6. Deploy to Kubernetes') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    & $env:KUBECTL apply -f deployment.yaml
                    if ($LASTEXITCODE -ne 0) {
                        throw "Kubernetes apply failed."
                    }

                    & $env:KUBECTL rollout status deployment/expense-v3 --timeout=180s
                    if ($LASTEXITCODE -ne 0) {
                        throw "V3 deployment did not become ready."
                    }
                '''
            }
        }

        stage('7. Verify Deployment') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    & $env:KUBECTL get deployment expense-v3
                    & $env:KUBECTL get pods -l app=expense-v3
                    & $env:KUBECTL get service expense-v3-service
                    & $env:DOCKER images $env:IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo 'Expense Tracker V3 pipeline completed successfully!'
        }
        failure {
            echo 'V3 pipeline failed. Check the first failed stage in Console Output.'
        }
    }
}
