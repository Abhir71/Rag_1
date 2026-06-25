pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/Abhir71/Rag_1.git'
        GIT_BRANCH  = 'main'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: "${GIT_BRANCH}",
                    url: "${GITHUB_REPO}",
                    credentialsId: 'github-credentials'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirments.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v
                '''
            }
        }

        stage('Push to GitHub') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-credentials',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git config user.email "jenkins@local"
                        git config user.name "Jenkins"
                        git remote set-url origin https://${GIT_USER}:${GIT_TOKEN}@github.com/Abhir71/Rag_1.git
                        git push origin main
                    '''
                }
            }
        }
    }

    post {
        success { echo '✅ Tests passed — pushed to GitHub!' }
        failure { echo '❌ Tests failed — push skipped.' }
    }
}