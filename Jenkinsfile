pipeline {
    agent any

    parameters {
        string(
            name: 'IMAGE_TAG',
            defaultValue: 'f373518c19c4c8b8db924b55885cbab9eaeab564',
            description: 'Immutable Git commit SHA published to Docker Hub'
        )
    }

    environment {
        IMAGE_REPOSITORY = 'saiprathapk17/hello-api'
    }

    stages {
        stage('Validate Image Tag') {
            steps {
                script {
                    if (!(params.IMAGE_TAG ==~ /^[0-9a-f]{40}$/)) {
                        error('IMAGE_TAG must be a complete 40-character Git SHA')
                    }
                }
            }
        }

        stage('Verify Image Exists') {
            steps {
                bat 'docker buildx imagetools inspect %IMAGE_REPOSITORY%:%IMAGE_TAG%'
            }
        }

        stage('Deploy to Staging') {
            steps {
                bat '''
                    kubectl set image deployment/hello-api hello-api=%IMAGE_REPOSITORY%:%IMAGE_TAG% -n staging
                    kubectl rollout status deployment/hello-api -n staging --timeout=120s
                    kubectl get pods -n staging
                '''
            }
        }

        stage('Test Staging') {
            steps {
                bat '''
                    kubectl get --raw "/api/v1/namespaces/staging/services/http:hello-api:80/proxy/health" | findstr healthy
                '''
            }
        }

        stage('Production Approval') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    input(
                        message: "Deploy image ${env.IMAGE_REPOSITORY}:${params.IMAGE_TAG} to production?",
                        ok: 'Deploy to Production'
                    )
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                bat '''
                    kubectl set image deployment/hello-api hello-api=%IMAGE_REPOSITORY%:%IMAGE_TAG% -n production
                    kubectl rollout status deployment/hello-api -n production --timeout=120s
                    kubectl get pods -n production
                '''
            }
        }

        stage('Test Production') {
            steps {
                bat '''
                    kubectl get --raw "/api/v1/namespaces/production/services/http:hello-api:80/proxy/health" | findstr healthy
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully: ${env.IMAGE_REPOSITORY}:${params.IMAGE_TAG}"
        }

        failure {
            echo 'Deployment failed. Review the failed stage before retrying.'
        }

        aborted {
            echo 'Deployment stopped before production promotion.'
        }
    }
}