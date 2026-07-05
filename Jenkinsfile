pipeline {
    agent any

    environment {
        PACKAGE_NAME = "flask-practice.tar.gz"
        NOTIFY_EMAIL = "your-email@example.com"
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Build') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            py -m venv .venv
                            call .venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            pytest -v
                        '''
                    } else {
                        bat '''
                            call .venv\\Scripts\\activate.bat
                            pytest -v
                        '''
                    }
                }
            }
        }

        stage('Package') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            tar --exclude='.git' --exclude='.venv' -czf "$PACKAGE_NAME" .
                        '''
                    } else {
                        powershell '''
                            if (Test-Path $env:PACKAGE_NAME) {
                                Remove-Item $env:PACKAGE_NAME -Force
                            }
                            Compress-Archive -Path app.py,requirements.txt,test_app.py,templates,Jenkinsfile,.github,README.md -DestinationPath flask-practice.zip -Force
                        '''
                    }
                }
                archiveArtifacts artifacts: "flask-practice.*", fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            mkdir -p /tmp/flask-practice-staging
                            tar -xzf "$PACKAGE_NAME" -C /tmp/flask-practice-staging
                            touch /tmp/flask-practice-staging/.deployed
                            echo "Application deployed to staging directory: /tmp/flask-practice-staging"
                        '''
                    } else {
                        powershell '''
                            $stagingDir = "$env:WORKSPACE\\staging-deploy"
                            if (Test-Path $stagingDir) {
                                Remove-Item $stagingDir -Recurse -Force
                            }
                            New-Item -ItemType Directory -Path $stagingDir | Out-Null
                            Expand-Archive -Path flask-practice.zip -DestinationPath $stagingDir -Force
                            New-Item -ItemType File -Path "$stagingDir\\.deployed" -Force | Out-Null
                            Write-Host "Application deployed to staging directory: $stagingDir"
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                try {
                    emailext(
                        to: "${NOTIFY_EMAIL}",
                        subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
                        body: "The Jenkins pipeline completed successfully. Build URL: ${BUILD_URL}"
                    )
                } catch (err) {
                    echo "Email notification skipped: ${err}"
                }
            }
        }
        failure {
            script {
                try {
                    emailext(
                        to: "${NOTIFY_EMAIL}",
                        subject: "FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
                        body: "The Jenkins pipeline failed. Review logs here: ${BUILD_URL}"
                    )
                } catch (err) {
                    echo "Email notification skipped: ${err}"
                }
            }
        }
    }
}
