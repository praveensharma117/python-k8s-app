pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"                // Registry (Docker Hub)
        DOCKERHUB_USER = "devpraveens"        // Your DockerHub username
        IMAGE_NAME = "python-k8s-app"         // App image name
        APP_NAME = "python-k8s-app"           // Helm release name
        KUBE_CONFIG = "/home/devopsadmin/.kube/config"   // Path to kubeconfig on Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/praveensharma117/python-k8s-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_PASS')]) {
                    sh """
                      echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin
                      docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withEnv(["KUBECONFIG=${KUBE_CONFIG}"]) {
                    sh """
                      helm upgrade --install $APP_NAME ./helm \
                        --namespace default \
                        --create-namespace \
                        --set image.repository=${DOCKERHUB_USER}/${IMAGE_NAME} \
                        --set image.tag=${BUILD_NUMBER}
                    """
                }
            }
        }
    }
}

