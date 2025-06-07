pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USERNAME = "primslepremier3"
        IMAGE_VERSION = "1.${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_HUB_USERNAME}/examen:${IMAGE_VERSION}"
        DOCKER_CONTAINER = "exam_con_virtualisation"
        CONTAINER_PORT = "8091"
        APP_PORT = "8000"
    }
    
    stages {
        stage("Checkout") {
            steps {
                git branch: 'master', 
                url: 'https://github.com/desire427/Exam_Con_Vir.git'
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
                        @echo off
                        echo %DOCKER_HUB_PASSWORD% | docker login -u %DOCKER_HUB_USER% --password-stdin || (
                            echo [ERREUR] Échec de l'authentification Docker Hub
                            exit 1
                        )
                        docker push $DOCKER_IMAGE || (
                            echo [ERREUR] Échec du push Docker
                            exit 1
                        )
                        """
                    }
                }
            }
        }
        
        stage("Deploy") {
            steps {
                script {
                    bat """
                    docker stop ${DOCKER_CONTAINER} 2> nul || echo "Aucun conteneur à arrêter"
                    docker rm ${DOCKER_CONTAINER} 2> nul || echo "Aucun conteneur à supprimer"
                    docker run -d --name ${DOCKER_CONTAINER} -p ${CONTAINER_PORT}:${APP_PORT} ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }
}