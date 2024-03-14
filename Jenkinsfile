pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'develop', description: 'Branch to build')
        string(name: 'URL', defaultValue: 'https://github.com/aviran355/counter-service.git', description: 'Git repository URL')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: params.BRANCH, url: params.URL, credentialsId: '01df9c87-6980-44c6-bcac-1cc01e3f2c38'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("counterapp:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Deploy and Run') {
            steps {
                script {
                    def branch = params.BRANCH
                    def imageName = "counterapp:${env.BUILD_NUMBER}"
                    
                    // Pull the Docker image
                    docker.image(imageName).pull()
                    
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
    }
}

