pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USERNAME = "primslepremier3"  // Doit correspondre à votre compte Docker Hub
        IMAGE_VERSION = "1.${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_HUB_USERNAME}/examen:${IMAGE_VERSION}"  // Nom cohérent
        DOCKER_CONTAINER = "exam_con_virtualisation"
        CONTAINER_PORT = "8091"  // Port hôte
        APP_PORT = "8000"        // Port conteneur (ajouté)
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
                        credentialsId: '20041705',  // Vérifiez cet ID dans Jenkins
                        usernameVariable: 'DOCKER_HUB_USER',
                        passwordVariable: 'DOCKER_HUB_PASSWORD'
                    )]) {
                        // Méthode plus fiable pour le login
                        bat 'docker login -u %DOCKER_HUB_USER% -p %DOCKER_HUB_PASSWORD%'
                        bat "docker push $DOCKER_IMAGE"
                    }
                }
            }
        }
        
        stage("Deploy") {
            steps {
                script {
                    bat """
                    docker stop ${DOCKER_CONTAINER} 2> nul || echo "Container already stopped"
                    docker rm ${DOCKER_CONTAINER} 2> nul || echo "Container not found"
                    docker run -d --name ${DOCKER_CONTAINER} -p ${CONTAINER_PORT}:${APP_PORT} ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }
}