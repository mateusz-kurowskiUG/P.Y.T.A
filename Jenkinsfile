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
    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Backend') {
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

        stage('Frontend') {
            agent { docker { image 'oven/bun:1.2.3' } }
            steps {
                script {
                    setBuildStatus("Building frontend...", "PENDING")
                }
                dir('frontend') {
                    sh 'bun install'
                    sh 'bun run build'
                }
                script {
                    setBuildStatus("Frontend build successful", "SUCCESS")
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
