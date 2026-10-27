pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select which Telemedicine version to build'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install and Test') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"
                    $version = $env:VERSION

                    Push-Location $version
                    try {
                        python -m pip install -r requirements.txt
                        if ($LASTEXITCODE -ne 0) {
                            throw "Dependency installation failed"
                        }

                        python -m pytest -v
                        if ($LASTEXITCODE -ne 0) {
                            throw "Tests failed"
                        }
                    }
                    finally {
                        Pop-Location
                    }
                '''
            }
        }

        stage('Build and Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        $env:DOCKER_TOKEN |
                            docker login --username $env:DOCKER_USER --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub login failed"
                        }

                        $version = $env:VERSION
                        $image = "$($env:DOCKER_USER)/telemedicine-devops:$version"

                        docker build -t $image ".\\$version"
                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker build failed"
                        }

                        docker push $image
                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker push failed"
                        }

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Selected version tested, built, and pushed successfully.'
        }
        failure {
            echo 'Pipeline failed. Inspect Console Output for the error.'
        }
    }
}
