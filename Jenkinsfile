pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USERNAME = "primslepremier2"
        IMAGE_VERSION = "1.${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_HUB_USERNAME}/tp-app:${IMAGE_VERSION}"
        DOCKER_CONTAINER = "ci-cd-html-css-app"
        CONTAINER_PORT = "8091" // Changement de port pour éviter les conflits
    }
    
    stages {
        stage("Checkout") {
            steps {
                git branch: 'master', 
                url: 'https://github.com/desire427/Exam_Con_Vir.git'
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
                        // Méthode sécurisée pour le login Docker
                        bat """
                        echo %DOCKER_HUB_PASSWORD% | docker login -u %DOCKER_HUB_USER% --password-stdin
                        docker push $DOCKER_IMAGE
                        """
                    }
                }
            }
        }
        
        stage("Deploy") {
            steps {
                script {
                    // Commande compatible Windows pour gérer les erreurs
                    bat """
                    docker container stop $DOCKER_CONTAINER 2> nul || echo "Container already stopped"
                    docker container rm $DOCKER_CONTAINER 2> nul || echo "Container not found"
                    docker container run -d --name $DOCKER_CONTAINER -p ${CONTAINER_PORT}:80 $DOCKER_IMAGE
                    """
                }
            }
        }
    }
}