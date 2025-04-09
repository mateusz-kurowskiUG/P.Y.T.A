pipeline {
    agent {
        docker { image 'node:latest' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
