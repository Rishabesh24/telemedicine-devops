
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select Telemedicine version'
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

        stage('Test Docker Hub Authentication') {
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

                        $docker = "C:\\Users\\Rishabesh\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"

                        if (!(Test-Path $docker)) {
                            throw "Docker executable not found: $docker"
                        }

                        Write-Host "Docker username: $env:DOCKER_USER"

                        if ([string]::IsNullOrWhiteSpace($env:DOCKER_TOKEN)) {
                            throw "Docker Hub token is empty"
                        }

                        Write-Host "Token is populated: True"
                        Write-Host "Testing Docker Hub authentication..."

                        $loginOutput = @(
                            $env:DOCKER_TOKEN |
                                & $docker login `
                                    --username $env:DOCKER_USER `
                                    --password-stdin 2>&1
                        )

                        $loginExitCode = $LASTEXITCODE

                        if ($loginExitCode -ne 0) {
                            $loginOutput | ForEach-Object {
                                Write-Host $_
                            }

                            throw "Docker Hub authentication failed."
                        }

                        Write-Host "Docker Hub authentication succeeded."

                        & $docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker Hub authentication succeeded.'
        }

        failure {
            echo 'FAILED: Check Console Output for the first error.'
        }

        always {
            echo 'Authentication diagnostic pipeline finished.'
        }
    }
}
