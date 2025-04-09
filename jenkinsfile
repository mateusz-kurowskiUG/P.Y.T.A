pipeline {
    agent {
        docker { image 'node:latest' }
    }
    stages {
        stage('Clone') {
            checkout scm
        }
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
