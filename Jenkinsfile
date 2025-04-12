void setBuildStatus(String message, String state) {
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/mateusz-kurowskiUG/P.Y.T.A"],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [
            $class: "ConditionalStatusResultSource",
            results: [[$class: "AnyBuildResult", message: message, state: state]]
        ]
    ])
}

pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = 'DOCKERHUB'
        DOCKER_IMAGE_NAME = 'push mateuszkurowski/p.y.t.a'
    }
    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Test backend') {
            agent { docker { image 'python:3.12' } }
            steps {
                script {
                    setBuildStatus("Running backend tests...", "PENDING")
                }
                sh 'pip install poetry'
                sh 'poetry --directory ./backend install --no-root'
                sh 'poetry --directory ./backend run coverage run -m pytest'
                sh 'poetry --directory ./backend run coverage report --fail-under=100'
            }
        }

        stage('Build backend') {
            agent { docker { image 'python:3.12' } }
            steps {
                script {
                    setBuildStatus("Building backend docker image...", "PENDING")
                }
                sh 'docker build -t ${DOCKER_IMAGE_NAME}/backend ./backend'
                script {
                    setBuildStatus("Backend docker image built successfully", "SUCCESS")
                }
            }
        }

        stage('Push backend image') {
            steps {
                script {
                    setBuildStatus("Pushing backend docker image...", "PENDING")
                }
                withCredentials([usernamePassword(credentialsId: "${DOCKER_HUB_CREDENTIALS}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh """
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push ${DOCKER_IMAGE_NAME}/backend
                    """
                }
                script {
                    setBuildStatus("Backend docker image pushed successfully", "SUCCESS")
                }
            }
        }

        stage('Frontend') {
            agent { dockerfile { dir 'frontend' } }
            steps {
                script {
                    setBuildStatus("Building frontend...", "PENDING")
                }
                dir('frontend') {
                    sh 'bun install'
                    sh 'chmod -R +x ./node_modules/.bin'
                    sh 'bun run build'
                }
                script {
                    setBuildStatus("Frontend build successful", "SUCCESS")
                }
            }
        }

        stage('Build frontend image') {
            agent { dockerfile { dir 'frontend' } }
            steps {
                script {
                    setBuildStatus("Building frontend docker image...", "PENDING")
                }
                sh 'docker build -t ${DOCKER_IMAGE_NAME}/frontend ./frontend'
                script {
                    setBuildStatus("Frontend docker image built successfully", "SUCCESS")
                }
            }
        }

        stage('Push frontend image') {
            steps {
                script {
                    setBuildStatus("Pushing frontend docker image...", "PENDING")
                }
                withCredentials([usernamePassword(credentialsId: "${DOCKER_HUB_CREDENTIALS}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh """
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push ${DOCKER_IMAGE_NAME}/frontend
                    """
                }
                script {
                    setBuildStatus("Frontend docker image pushed successfully", "SUCCESS")
                }
            }
        }
    }

    post {
        success {
            script {
                setBuildStatus("Build succeeded", "SUCCESS")
            }
        }
        failure {
            script {
                setBuildStatus("Build failed", "FAILURE")
            }
        }
    }
}
