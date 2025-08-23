pipeline {
  agent any

  environment {
    DOCKERHUB_USER = "devpraveens"
    IMAGE_NAME     = "python-k8s-app"
    IMAGE_TAG      = "${BUILD_NUMBER}"
    KUBECONFIG     = "/var/lib/jenkins/.kube/config"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/praveensharma117/python-k8s-app.git'
      }
    }

    stage('Build Image') {
      steps {
        script {
          docker.build("${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}")
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_PASS')]) {
          sh '''
            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
            docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
          '''
        }
      }
    }

    stage('Deploy with Helm') {
      steps {
        sh '''
          helm upgrade --install python-k8s-app ./helm \
            --set image.repository=${DOCKERHUB_USER}/${IMAGE_NAME} \
            --set image.tag=${IMAGE_TAG}
        '''
      }
    }
  }

  post {
    always {
      sh '''
        kubectl get pods -o wide
        kubectl get svc python-k8s-app
        kubectl get ingress python-k8s-ingress -o yaml | sed -n '1,80p'
      '''
    }
  }
}

