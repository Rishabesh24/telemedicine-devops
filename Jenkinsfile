
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

                    $python = "C:\\Users\\Rishabesh\\AppData\\Local\\Python\\bin\\python.exe"

                    if (!(Test-Path $python)) {
                        throw "Python executable not found: $python"
                    }

                    $version = $env:VERSION
                    Push-Location $version

                    try {
                        & $python -m venv .venv
                        if ($LASTEXITCODE -ne 0) {
                            throw "Virtual environment creation failed"
                        }

                        $venvPython = Join-Path (Get-Location) ".venv\\Scripts\\python.exe"

                        & $venvPython -m pip install -r requirements.txt
                        if ($LASTEXITCODE -ne 0) {
                            throw "Dependency installation failed"
                        }

                        & $venvPython -m pytest -v
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

                        Write-Host "Docker username: $env:DOCKER_USER"
                        Write-Host "Token populated: $(-not [string]::IsNullOrWhiteSpace($env:DOCKER_TOKEN))"

                        $docker = "C:\\Users\\Rishabesh\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"

                        if (!(Test-Path $docker)) {
                            throw "Docker executable not found: $docker"
                        }

                        $version = $env:VERSION
                        $image = "$($env:DOCKER_USER)/telemedicine-devops:$version"

                        $env:DOCKER_TOKEN |
                            & $docker login --username $env:DOCKER_USER --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub login failed"
                        }

                        try {
                            & $docker build -t $image ".\\$version"
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker build failed for $version"
                            }

                            & $docker push $image
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker push failed for $version"
                            }
                        }
                        finally {
                            & $docker logout
                        }
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and the selected image was pushed to Docker Hub.'
        }

        failure {
            echo 'FAILED: Check Console Output for the first error.'
        }
    }
}
