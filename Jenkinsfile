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
    agent {
        docker { image 'python:3.12' }
    }
    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                script {
                    setBuildStatus("Running tests...", "PENDING")
                }
                sh 'pip install poetry'
                sh 'poetry --directory ./backend install --no-root'
                sh 'poetry --directory ./backend run coverage run -m pytest'
                sh 'poetry --directory ./backend run coverage report --fail-under=100'
            }
        }
    }
    post {
        always {
            echo "====++++always++++===="
        }
        success {
            script {
                setBuildStatus("Build succeeded", "SUCCESS")
            }
            echo "====++++only when successful++++===="
        }
        failure {
            script {
                setBuildStatus("Build failed", "FAILURE")
            }
            echo "====++++only when failed++++===="
        }
    }
}
