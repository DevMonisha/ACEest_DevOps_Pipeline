pipeline {
    agent {
        docker {
            image 'python:3.10-bullseye'
            args '-u root'      // run as root
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

        stage('Install system dependencies') {
            steps {
                echo "Installing Tkinter + Xvfb inside Docker agent..."
                sh '''
                    apt-get update
                    apt-get install -y python3-tk xvfb xauth xfonts-base zip
                '''
            }
        }

        stage('Set up Python venv') {
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

                    # Start virtual display for Tkinter
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
            echo "✅ Build Successful!"
        }
        failure {
            echo "❌ Build Failed!"
        }
    }
}
