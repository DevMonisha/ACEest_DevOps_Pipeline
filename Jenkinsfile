pipeline {
    agent any

    environment {
        APP_VERSION = "v1.3"
        PYTHON_ENV = "${WORKSPACE}/venv"
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
                    pip install --upgrade pip
                    pip install -r requirements.txt
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
