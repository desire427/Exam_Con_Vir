pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USERNAME = "primslepremier2"  // Votre vrai username Docker Hub
        IMAGE_VERSION = "1.${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_HUB_USERNAME}/tp-app:${IMAGE_VERSION}" // Format corrigé
        DOCKER_CONTAINER = "ci-cd-html-css-app"
    }
    
    stages {
        stage("Checkout") {
            steps {
                git branch: 'master', url: 'https://github.com/desire427/Exam_Con_Vir.git'
            }
        }
        
        stage("Test") {
            steps {
                echo "Tests en cours"
            }
        }
        
        stage("Build Docker Image") {
            steps {
                script {
                    bat "docker build -t $DOCKER_IMAGE ."
                }
            }
        }
        
        stage("Push image to Docker Hub") {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: '20041705', 
                        usernameVariable: 'DOCKER_HUB_USER', 
                        passwordVariable: 'DOCKER_HUB_PASSWORD'
                    )]) {
                        bat """
                        docker login -u %DOCKER_HUB_USER% -p %DOCKER_HUB_PASSWORD%
                        docker push $DOCKER_IMAGE
                        """
                    }
                }
            }
        }
        
        stage("Deploy") {
            steps {
                script {
                    bat """
                    docker container stop $DOCKER_CONTAINER || true
                    docker container rm $DOCKER_CONTAINER || true
                    docker container run -d --name $DOCKER_CONTAINER -p 8090:80 $DOCKER_IMAGE
                    """
                }
            }
        }
    }
}