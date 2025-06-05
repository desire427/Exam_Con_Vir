// Déclaration du pipeline Jenkins
pipeline {
    // Exécute le pipeline sur n'importe quel agent
    agent any
    // Déclarer les variables d'environnement globales 
    environment {
        DOCKER_USERNAME = "examen" // username docker
        IMAGE_VERSION = "1.${BUILD_NUMBER}"  // version dynamique de l’image
        DOCKER_IMAGE = "${DOCKER_USERNAME}/tp-app:${IMAGE_VERSION}" // nom de l’image docker
        DOCKER_CONTAINER = "ci-cd-html-css-app"  // nom du conteneur
    }
    // Les étapes du pipeline
    stages {
        // Étape 1 : Récupération du code source depuis GitHub
        stage("Checkout") {
            steps {
                git branch: 'master', url: 'https://github.com/desire427/Exam_Con_Vir.git'
            }
        }
        // Étape 2 : Exécution des tests
        stage("Test") {
            steps {
                echo "Tests en cours"
            }
        }
        // Étape 3 : Création de l'image Docker
        stage("Build Docker Image") {
            steps {
                script {
                    bat "docker build -t $DOCKER_IMAGE ."
                }
            }
        }
        // Étape 4 : Publication de l'image sur Docker Hub
        stage("Push image to Docker Hub") {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: '20041705', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]){
                    bat """
                    docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}
                    echo 'Docker login successful'
                    docker push $DOCKER_IMAGE
                    """
                    }
                }
            }
        }
        // Étape 5 : Déploiement de l'application
        stage("Deploy") {
            steps {
                script {
                    bat """
                    # Arrête le conteneur s'il existe
                    docker container stop $DOCKER_CONTAINER || true
                    # supprime le conteneur s'il existe
                    docker container rm $DOCKER_CONTAINER || true
                    # Lance un nouveau conteneur en mode détaché(en arrière-plan )
                    docker container run -d --name $DOCKER_CONTAINER -p 8090:80 $DOCKER_IMAGE
                    """
                }
            }
        }
    }
}