pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins/label: kaniko
spec:
  serviceAccountName: jenkins-sa
  containers:
    - name: jnlp
      image: jenkins/inbound-agent:latest
      args: ['$(JENKINS_SECRET)', '$(JENKINS_NAME)']
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

    - name: kaniko
      image: gcr.io/kaniko-project/executor:debug
      command: ['sh', '-c', 'sleep infinity']
      tty: true
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
        - name: harbor-creds
          mountPath: /kaniko/.docker/config.json
          subPath: config.json

    - name: kubectl
      image: lachlanevenson/k8s-kubectl:latest
      command: ['sh', '-c', 'sleep infinity']
      tty: true
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

    - name: sonar
      image: sonarsource/sonar-scanner-cli:latest
      command: ['sh', '-c', 'sleep infinity']
      tty: true
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent

  volumes:
    - name: harbor-creds
      secret:
        secretName: harbor-creds
        items:
          - key: .dockerconfigjson
            path: config.json
    - name: workspace-volume
      emptyDir: {}
'''
    }
  }

  environment {
    APP_NAME         = "nuge"
    GIT_REPO         = "https://github.com/sebastined/nuge.git"
    REGISTRY         = "harbor.int.sebastine.ng/900"
    IMAGE_NAME       = "${REGISTRY}/${APP_NAME}"
    TAG              = "${BUILD_NUMBER}"
    K8S_NAMESPACE    = "prod00"
    SONAR_URL        = "http://sonar.int.sebastine.ng"
    SONARQUBE        = "SonarQube"
    SONAR_AUTH_TOKEN = credentials('sonarqube')
  }

  stages {

    stage('Prepare workspace') {
      steps {
        container('jnlp') {
          sh '''
            git config --global --add safe.directory /home/jenkins/agent || true
          '''
        }
      }
    }

    stage('Checkout Source') {
      steps {
        container('jnlp') {
          git branch: 'master', url: "${GIT_REPO}"
        }
      }
    }

    stage('SonarQube Analysis') {
      steps {
        container('sonar') {
          withSonarQubeEnv("${SONARQUBE}") {
            sh '''
              sonar-scanner \
                -Dsonar.projectKey=${APP_NAME} \
                -Dsonar.sources=. \
                -Dsonar.host.url=${SONAR_URL} \
                -Dsonar.token=${SONAR_AUTH_TOKEN}
            '''
          }
        }
      }
    }

    stage('Build & Push Image with Kaniko') {
      steps {
        container('kaniko') {
          sh '''
            IMAGE_DEST="${IMAGE_NAME}:${TAG}"
            echo "Building ${IMAGE_DEST} with Kaniko..."
            /kaniko/executor \
              --context "$PWD" \
              --dockerfile Dockerfile \
              --destination "${IMAGE_DEST}" \
              --cache=true \
              --insecure --skip-tls-verify
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh '''
            echo "Deploying ${APP_NAME}:${TAG} to ${K8S_NAMESPACE}..."
            kubectl -n ${K8S_NAMESPACE} set image deployment/${APP_NAME}-deploy ${APP_NAME}-container=${IMAGE_NAME}:${TAG} || \
              kubectl -n ${K8S_NAMESPACE} create deployment ${APP_NAME}-deploy --image=${IMAGE_NAME}:${TAG}

            kubectl -n ${K8S_NAMESPACE} rollout status deployment/${APP_NAME}-deploy --timeout=120s || true

            kubectl -n ${K8S_NAMESPACE} expose deployment ${APP_NAME}-deploy \
              --port=8080 --type=ClusterIP --dry-run=client -o yaml | kubectl apply -f -
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Successfully deployed ${APP_NAME}:${TAG}"
    }
    failure {
      echo "❌ Pipeline failed — check logs for details"
    }
  }
}
