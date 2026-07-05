# Student Registration Flask App - CI/CD Assignment

This repository contains a simple Flask web application for managing student records. The assignment deliverables are included:

- `Jenkinsfile` for Jenkins CI/CD
- `.github/workflows/flask-ci-cd.yml` for GitHub Actions CI/CD
- Pytest test suite in `test_app.py`
- Documentation for prerequisites, setup, triggers, notifications, and deployment

## Application Overview

The app supports basic student management:

- View student records
- Add a student
- Update student details
- Delete a student

Technology used:

- Python
- Flask
- MongoDB with Flask-PyMongo
- Pytest
- Jenkins
- GitHub Actions

## Local Setup

Clone the repository:

```bash
git clone <your-github-repository-url>
cd flask-cicd-assignment
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file:

```env
MONGO_URI=mongodb://localhost:27017/student_db
SECRET_KEY=change-this-secret-key
```

Run the application:

```bash
python app.py
```

Open the app at:

```text
http://localhost:5000
```

Run tests:

```bash
pytest -v
```

The tests use an in-memory fake database, so a live MongoDB server is not required for CI test execution.

## Jenkins CI/CD Pipeline

The Jenkins pipeline is defined in `Jenkinsfile`.

### Jenkins Prerequisites

Install and configure:

- Jenkins
- Git
- Python 3 and pip
- Jenkins Pipeline plugin
- GitHub plugin
- Email Extension plugin
- SMTP email settings in Jenkins

### Jenkins Job Setup

1. Fork this repository to your GitHub account.
2. In Jenkins, create a new Pipeline job.
3. Select `Pipeline script from SCM`.
4. Choose Git as the SCM.
5. Add your GitHub repository URL.
6. Set the branch to `*/main`.
7. Set the script path to `Jenkinsfile`.
8. Save the job and run `Build Now`.

### Jenkins Stages

The Jenkins pipeline contains these stages:

| Stage | Purpose |
| --- | --- |
| Build | Installs Python dependencies with pip |
| Test | Runs the Pytest test suite |
| Package | Creates a deployable application package |
| Deploy | Deploys the package to a staging folder after tests pass |

### Jenkins Trigger

The `Jenkinsfile` includes:

```groovy
triggers {
    githubPush()
    pollSCM('H/5 * * * *')
}
```

For GitHub push triggers, add this webhook in your GitHub repository:

```text
http://<your-jenkins-server-url>/github-webhook/
```

Set the webhook event to:

```text
Just the push event
```

### Jenkins Email Notifications

The pipeline sends email on success and failure using `emailext`.

Update this value in `Jenkinsfile`:

```groovy
NOTIFY_EMAIL = "your-email@example.com"
```

Also configure SMTP settings in Jenkins:

```text
Manage Jenkins -> System -> Extended E-mail Notification
```

## GitHub Actions CI/CD Pipeline

The GitHub Actions workflow is defined in:

```text
.github/workflows/flask-ci-cd.yml
```

### Branch Requirements

The repository should have:

- `main` branch
- `staging` branch

Create the staging branch if it does not exist:

```bash
git checkout -b staging
git push origin staging
```

### GitHub Actions Workflow Triggers

The workflow runs on:

- Push to `main`
- Push to `staging`
- Pull requests to `main` or `staging`
- Version tags such as `v1.0.0`

### GitHub Actions Jobs

| Job | Purpose |
| --- | --- |
| Install Dependencies and Run Tests | Installs Python dependencies and runs Pytest |
| Build Application Package | Creates a deployable package and uploads it as an artifact |
| Deploy to Staging | Runs when changes are pushed to the `staging` branch |
| Deploy to Production | Runs when a version tag such as `v1.0.0` is pushed |

### GitHub Secrets

Add secrets from:

```text
GitHub repository -> Settings -> Secrets and variables -> Actions -> New repository secret
```

For staging deployment:

| Secret | Description |
| --- | --- |
| `STAGING_HOST` | Staging server hostname or IP address |
| `STAGING_USER` | SSH username for staging server |
| `STAGING_PATH` | Deployment path on staging server |
| `STAGING_SSH_KEY` | Private SSH key for staging deployment |

For production deployment:

| Secret | Description |
| --- | --- |
| `PRODUCTION_HOST` | Production server hostname or IP address |
| `PRODUCTION_USER` | SSH username for production server |
| `PRODUCTION_PATH` | Deployment path on production server |
| `PRODUCTION_SSH_KEY` | Private SSH key for production deployment |

If these secrets are not configured, the deploy jobs still create a local deployment package during the workflow run. This is useful for classroom demonstration screenshots. For real deployment, configure the secrets above.

### Deploy to Staging

Push changes to the `staging` branch:

```bash
git checkout staging
git merge main
git push origin staging
```

### Deploy to Production

Create and push a release tag:

```bash
git checkout main
git tag v1.0.0
git push origin v1.0.0
```

## Required Screenshots

Include these screenshots in the final assignment submission:

- Jenkins pipeline showing Build, Test, Package, and Deploy stages
- Jenkins console output showing successful test execution
- GitHub Actions workflow run on `main`
- GitHub Actions workflow run on `staging`
- GitHub Actions workflow run for a release tag such as `v1.0.0`

## Submission

Submit a text, Word, or PDF file containing your GitHub repository URL:

```text
GitHub Repository URL: https://github.com/kautikbhardwaj/flask-cicd-assignment
```

Upload that file to Vlearn.

## License

MIT License
