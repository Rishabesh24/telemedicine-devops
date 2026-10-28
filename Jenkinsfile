
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

                        $docker = "C:\\Users\\Rishabesh\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"

                        if (!(Test-Path $docker)) {
                            throw "Docker executable not found: $docker"
                        }

                        $version = $env:VERSION
                        $image = "$($env:DOCKER_USER)/telemedicine-devops:$version"

                        if ([string]::IsNullOrWhiteSpace($env:DOCKER_TOKEN)) {
                            throw "Docker Hub token is empty"
                        }

                        $tokenFile = Join-Path $env:TEMP (
                            "docker-token-" + [guid]::NewGuid().ToString() + ".txt"
                        )
                        $loginFile = Join-Path $env:TEMP (
                            "docker-login-" + [guid]::NewGuid().ToString() + ".cmd"
                        )

                        try {
                            $utf8 = New-Object System.Text.UTF8Encoding($false)
                            [System.IO.File]::WriteAllText(
                                $tokenFile, $env:DOCKER_TOKEN, $utf8
                            )

                            $command = '"' + $docker +
                                '" login --username "' + $env:DOCKER_USER +
                                '" --password-stdin < "' + $tokenFile + '"'

                            [System.IO.File]::WriteAllText(
                                $loginFile, $command, $utf8
                            )

                            & $env:ComSpec /d /c $loginFile
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker Hub login failed"
                            }

                            Write-Host "Docker Hub login succeeded."

                            & $docker build -t $image ".\\$version"
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker build failed for $version"
                            }

                            & $docker push $image
                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker push failed for $version"
                            }

                            Write-Host "Successfully pushed: $image"
                        }
                        finally {
                            Remove-Item $tokenFile -Force -ErrorAction SilentlyContinue
                            Remove-Item $loginFile -Force -ErrorAction SilentlyContinue
                            & $docker logout
                        }
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image was pushed.'
        }
        failure {
            echo 'FAILED: Check Console Output for the first error.'
        }
    }
}
