pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"          // change if using another registry
        DOCKERHUB_USER = "devpraveens"
        IMAGE_NAME = "python-k8s-app"
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
                sh """
                  helm upgrade --install python-k8s-app ./helm \
                  --set image.repository=${DOCKERHUB_USER}/${IMAGE_NAME} \
                  --set image.tag=${BUILD_NUMBER}
                """
            }
        }
    }
}
