pipeline {
  agent any

  stages {
    stage('Backend Syntax Check') {
      steps {
        dir('backend') {
          sh 'python -m compileall app'
        }
      }
    }

    stage('Frontend Build') {
      steps {
        dir('frontend') {
          sh 'npm install'
          sh 'npm run build'
        }
      }
    }

    stage('Docker Compose Config') {
      steps {
        sh 'docker compose config'
      }
    }
  }
}

