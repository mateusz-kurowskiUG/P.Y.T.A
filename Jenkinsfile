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
                sh 'pip install poetry'
                sh 'poetry --directory ./backend install --no-root'
                sh 'poetry --directory ./backend run coverage run -m pytest'
                sh 'poetry --directory ./backend run coverage report --fail-under=100'
            }
        }
    }
}
