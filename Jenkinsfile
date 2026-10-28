
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

                        if ([string]::IsNullOrWhiteSpace($env:DOCKER_USER)) {
                            throw "Docker Hub username is empty"
                        }

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
                                $tokenFile,
                                $env:DOCKER_TOKEN,
                                $utf8
                            )

                            $dockerEscaped = $docker.Replace('"', '""')
                            $tokenEscaped = $tokenFile.Replace('"', '""')

                            $command = '"' + $dockerEscaped +
                                '" login --username "' + $env:DOCKER_USER +
                                '" --password-stdin < "' + $tokenEscaped + '"'

                            [System.IO.File]::WriteAllText(
                                $loginFile,
                                $command,
                                $utf8
                            )

                            Write-Host "Testing Docker Hub login for $env:DOCKER_USER"

                            & $env:ComSpec /d /c $loginFile
                            $loginExitCode = $LASTEXITCODE

                            if ($loginExitCode -ne 0) {
                                throw "Docker Hub authentication failed."
                            }

                            Write-Host "Docker Hub authentication succeeded."

                            & $docker logout
                        }
                        finally {
                            Remove-Item $tokenFile -Force -ErrorAction SilentlyContinue
                            Remove-Item $loginFile -Force -ErrorAction SilentlyContinue
                        }
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
            echo 'Telemedicine CI/CD diagnostic pipeline finished.'
        }
    }
}
