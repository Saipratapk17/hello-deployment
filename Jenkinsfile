pipeline {
    agent any

    stages {
        stage('Verify Jenkins Environment') {
            steps {
                bat 'whoami'
                bat 'git --version'
                bat 'docker version'
                bat 'kubectl version --client'
                bat 'kubectl config current-context'
                bat 'kubectl get nodes'
            }
        }
    }
}