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

        stage('Set up Python environment') {
            steps {
                echo 'Setting up virtual environment and dependencies...'
                sh '''
                apt-get update

                # Install Xvfb + GUI dependencies
                apt-get install -y xvfb xauth xfonts-base python3-tk

                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Pytest unit tests in headless mode...'
                sh '''
                . venv/bin/activate

                # Start virtual display
                export DISPLAY=:99
                Xvfb :99 -screen 0 1024x768x16 &
                sleep 3

                pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Artifact') {
            steps {
                echo "Packaging build artifacts..."
                sh '''
                mkdir -p build
                zip -r build/ACEest_Fitness_${APP_VERSION}.zip app/ tests/ requirements.txt
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'build/*.zip', fingerprint: true
                echo "Artifact archived successfully!"
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
