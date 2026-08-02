# Containerized Payment Application

This project is a complete DevOps assignment that containerizes a Python GUI, a mock Payment API, and MongoDB using Docker and Docker Compose. It also includes CI/CD setup via Jenkins and GitHub Security Actions.

## Architecture

The application runs as 3 Docker containers:
1. **payment-gui**: A Python Flask application serving as the frontend.
2. **payment-api**: A Python Flask REST API that simulates the existing payment service.
3. **mongodb**: Database to store the payment records.

## Local Setup (Phase 1)

### Prerequisites
- Docker and Docker Compose installed.

### Steps to Run Locally
1. Clone the repository.
2. Navigate to the project directory: `cd DevOPS`
3. Run the containers:
   ```bash
   docker-compose up --build -d
   ```
4. Access the GUI at `http://localhost:5000`
5. The API is accessible internally and at `http://localhost:8080/api/payments`.

## Cloud Deployment (Phase 2) - AWS EC2 via Jenkins

### 1. GitHub Setup
- The repository includes `.github/workflows/security.yml` which automatically runs **CodeQL** and **Dependabot** scans on every push to the `main` branch.

### 2. Jenkins CI/CD Setup
A `Jenkinsfile` is provided for the CI/CD pipeline.

**Jenkins Prerequisites & Credentials:**
1. **Docker Hub**: Add your Docker Hub credentials in Jenkins with ID `dockerhub-creds`.
2. **AWS EC2 SSH Key**: 
   - You mentioned using a `.ppk` key for AWS deployment. 
   - Jenkins natively supports OpenSSH `.pem` keys better via the **SSH Agent Plugin**. 
   - **Recommendation**: Convert your `.ppk` key to a `.pem` key using PuTTYgen (Export -> OpenSSH key).
   - Add this private key to Jenkins Credentials with ID `aws-ec2-key` (Kind: SSH Username with private key).
3. **Plugins Required in Jenkins**:
   - Docker Pipeline
   - SSH Agent Plugin

**Pipeline Stages:**
1. **Checkout**: Pulls code from GitHub.
2. **Build**: Builds the Docker image for the Python GUI.
3. **Push**: Pushes the image to Docker Hub.
4. **Deploy**: SSHes into the AWS EC2 instance, copies `docker-compose.yml`, and runs `docker-compose up -d`.

### Customizing for Your Environment
- In `Jenkinsfile`, change `yourusername/payment-gui:latest` to your actual Docker Hub username.
- Update `EC2_HOST` in the `Jenkinsfile` to your AWS EC2 Public IP or DNS.
- Change the `git url` in the `Checkout` stage to your actual GitHub repository URL.
