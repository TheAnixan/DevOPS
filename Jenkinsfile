pipeline {
    agent any

    environment {
        // Assume Docker credentials ID is 'dockerhub-creds'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        // Assume EC2 SSH Key ID is 'aws-ec2-key'
        EC2_SSH_KEY = credentials('aws-ec2-key')
        EC2_USER = 'ubuntu' // Change this based on AMI
        EC2_HOST = '3.107.21.198' // Change this to your Elastic IP
        DOCKER_IMAGE = 'anixan/payment-gui:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/TheAnixan/DevOPS.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Payment GUI Image..."
                    sh "docker build -t ${DOCKER_IMAGE} ./gui"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Logging into Docker Hub..."
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    
                    echo "Pushing Image..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                script {
                    echo "Deploying via SSH..."
                    // Create a temporary script for deployment
                    sh '''
                    cat << 'EOF' > deploy.sh
                    #!/bin/bash
                    # Ensure docker and docker-compose are installed on the host
                    mkdir -p ~/app
                    EOF
                    '''
                    
                    // The ssh-agent plugin is used here to load the PPK/PEM key securely
                    sshagent(credentials: ['aws-ec2-key']) {
                        // Ensure app directory exists on the remote server
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'mkdir -p ~/app'"

                        // Copy the docker-compose file
                        sh "scp -o StrictHostKeyChecking=no docker-compose.yml ${EC2_USER}@${EC2_HOST}:~/app/docker-compose.yml"
                        
                        // Execute docker-compose up on the server
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ~/app && sudo docker compose pull && sudo docker compose up -d'"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker credentials...'
            sh 'docker logout'
        }
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
