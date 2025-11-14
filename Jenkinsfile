pipeline {
    agent {
        docker {
            image 'python:3.10-bullseye'   // includes python3
            args '-u root'                 // allow apt-get install
        }
    }

    environment {
        APP_VERSION = "v1.3"
        PYTHON_ENV = "${WORKSPACE}/venv"

        SSL_CERT_FILE = "/etc/ssl/certs/ca-certificates.crt"
        REQUESTS_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Fetching latest code..."
                git branch: 'main', url: 'https://github.com/DevMonisha/ACEest_DevOps_Pipeline.git'
            }
        }

        stage('Install System Dependencies') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y xvfb python3-tk xauth xfonts-base unzip
                '''
            }
        }

        stage('Set up Python environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running pytest in headless mode..."
                sh '''
                    . venv/bin/activate

                    # Start X virtual display for tkinter
                    Xvfb :99 -screen 0 1024x768x16 &
                    export DISPLAY=:99

                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Artifact') {
            steps {
                sh '''
                    mkdir -p build
                    zip -r build/ACEest_Fitness_${APP_VERSION}.zip app/ tests/ requirements.txt
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'build/*.zip', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Build and test passed successfully!"
        }
        failure {
            echo "❌ Build failed. Please check logs."
        }
    }
}
