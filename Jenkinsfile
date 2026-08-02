pipeline {
    agent any

    environment {
        // Assume Docker credentials ID is 'dockerhub-creds'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        // Assume EC2 SSH Key ID is 'aws-ec2-key'
        // EC2_SSH_KEY = credentials('aws-ec2-key')
        EC2_USER = 'ubuntu' // Change this based on AMI
        EC2_HOST = 'your-ec2-public-ip' // Change this to your Elastic IP
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

        // AWS Deployment stage temporarily removed
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
