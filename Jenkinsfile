pipeline {
    agent {
        docker { image 'node:latest' }
    }
    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
