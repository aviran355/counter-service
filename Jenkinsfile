pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'develop', description: 'Branch to build')
        string(name: 'URL', defaultValue: 'https://github.com/aviran355/counter-service.git', description: 'Git repository URL')
    }
    
    environment {
        DOCKER_CREDENTIALS_ID = 'd13d2dcd-466d-466c-85db-430b46f34af9'
        DOCKER_HUB_REPO = 'aviranmashiach/counterproject'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: params.BRANCH, url: params.URL, credentialsId: '01df9c87-6980-44c6-bcac-1cc01e3f2c38'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    def dockerImage = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
                    
                    // Tag the Docker image with Docker Hub repository
                    sh "docker tag ${dockerImage} ${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
                    
                    // Login to Docker Hub
                    withDockerRegistry(credentialsId: DOCKER_CREDENTIALS_ID, url: 'https://index.docker.io/v1/') {
                        // Push the Docker image to Docker Hub
                        sh "docker push ${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
        
        stage('Deploy and Run') {
            steps {
                script {
                    def branch = params.BRANCH
                    def imageName = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
                    
                    // Pull the Docker image
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        docker.image(imageName).pull()
                    }
                    
                    // Stop and remove any existing containers with the same name
                    sh "docker stop counter-service || true"
                    sh "docker rm counter-service || true"
                    
                    // Run the Docker container
                    docker.image(imageName).run("-d --name counter-service -p 80:5000")
                    
                    // Wait for the container to start
                    sh 'sleep 10'
                    
                    // Check if the service is ready
                    def serviceReady = sh(script: 'curl -s http://ec2-18-159-208-86.eu-central-1.compute.amazonaws.com/ | grep "POST request count"', returnStatus: true) == 0
                    if (serviceReady) {
                        echo 'Service is ready!'
                    } else {
                        error 'Service is not ready!'
                    }
                }
            }
        }
        stage('Send POST Request') {
            steps {
                script {
                    sh 'curl -X POST http://ec2-18-159-208-86.eu-central-1.compute.amazonaws.com/'
                }
            }
        }
    }
}
