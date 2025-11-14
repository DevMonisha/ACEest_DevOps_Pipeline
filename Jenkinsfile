pipeline {
    agent any

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
                echo "Installing Xvfb + Tk..."
                sh '''
                    # Jenkins default user is root inside container → apt works
                    apt-get update
                    apt-get install -y xvfb python3-tk xauth xfonts-base unzip
                '''
            }
        }

        stage('Set up Python environment') {
            steps {
                echo "Creating venv and installing dependencies..."
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
                echo "Running pytest in HEADLESS mode..."
                sh '''
                    . venv/bin/activate

                    # Start a virtual display for Tkinter tests
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
