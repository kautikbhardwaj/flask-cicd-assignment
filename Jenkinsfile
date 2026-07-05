pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        PACKAGE_NAME = "flask-practice.tar.gz"
        STAGING_DIR = "/tmp/flask-practice-staging"
        NOTIFY_EMAIL = "your-email@example.com"
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv "$VENV_DIR"
                    . "$VENV_DIR/bin/activate"
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . "$VENV_DIR/bin/activate"
                    pytest -v
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                    tar --exclude='.git' --exclude='.venv' -czf "$PACKAGE_NAME" .
                '''
                archiveArtifacts artifacts: "${PACKAGE_NAME}", fingerprint: true
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    mkdir -p "$STAGING_DIR"
                    tar -xzf "$PACKAGE_NAME" -C "$STAGING_DIR"
                    touch "$STAGING_DIR/.deployed"
                    echo "Application deployed to staging directory: $STAGING_DIR"
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: "${NOTIFY_EMAIL}",
                subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
                body: "The Jenkins pipeline completed successfully. Build URL: ${BUILD_URL}"
            )
        }
        failure {
            emailext(
                to: "${NOTIFY_EMAIL}",
                subject: "FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
                body: "The Jenkins pipeline failed. Review logs here: ${BUILD_URL}"
            )
        }
    }
}
