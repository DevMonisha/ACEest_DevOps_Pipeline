pipeline {
    agent any

    environment {
        APP_VERSION = "v1.3"
        PYTHON_ENV = "${WORKSPACE}/venv"

        // 👇 Add SSL environment variables globally
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
                echo "Setting up virtual environment and dependencies..."
                sh '''
                    python3 -m venv $PYTHON_ENV
                    . $PYTHON_ENV/bin/activate

                    # Ensure system certificates are recognized
                    export SSL_CERT_FILE=$SSL_CERT_FILE
                    export REQUESTS_CA_BUNDLE=$REQUESTS_CA_BUNDLE

                    pip install --upgrade pip
                    pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Pytest unit tests..."
                sh '''
                    . $PYTHON_ENV/bin/activate
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
