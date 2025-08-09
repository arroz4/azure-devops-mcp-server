# Docker build and run script for ADO MCP Server (PowerShell)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("build", "run", "stop", "logs", "shell", "clean")]
    [string]$Command
)

$IMAGE_NAME = "ado-mcp-server"
$TAG = "latest"
$CONTAINER_NAME = "ado-mcp-server"
$PORT = "8000"

function Show-Usage {
    Write-Host "Usage: .\docker-script.ps1 [build|run|stop|logs|shell|clean]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  build   - Build the Docker image"
    Write-Host "  run     - Run the container"
    Write-Host "  stop    - Stop and remove the container"
    Write-Host "  logs    - Show container logs"
    Write-Host "  shell   - Open shell in running container"
    Write-Host "  clean   - Remove container and image"
    Write-Host ""
}

function Invoke-Build {
    Write-Host "Building Docker image: $IMAGE_NAME`:$TAG"
    docker build -f docker/Dockerfile -t "$IMAGE_NAME`:$TAG" .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Build complete!" -ForegroundColor Green
    } else {
        Write-Host "Build failed!" -ForegroundColor Red
        exit 1
    }
}

function Start-Container {
    Write-Host "Starting container: $CONTAINER_NAME"
    
    # Stop existing container if running
    $existing = docker ps -q -f "name=$CONTAINER_NAME"
    if ($existing) {
        Write-Host "Stopping existing container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    }
    
    # Run new container
    docker run -d `
        --name $CONTAINER_NAME `
        -p "$PORT`:$PORT" `
        --env-file .env `
        "$IMAGE_NAME`:$TAG"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Container started! Access at http://localhost:$PORT" -ForegroundColor Green
        Write-Host "Health check: http://localhost:$PORT/health" -ForegroundColor Green
    } else {
        Write-Host "Failed to start container!" -ForegroundColor Red
        exit 1
    }
}

function Stop-Container {
    Write-Host "Stopping container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME 2>$null
    docker rm $CONTAINER_NAME 2>$null
    Write-Host "Container stopped and removed!" -ForegroundColor Green
}

function Show-Logs {
    Write-Host "Showing logs for: $CONTAINER_NAME"
    docker logs -f $CONTAINER_NAME
}

function Open-Shell {
    Write-Host "Opening shell in: $CONTAINER_NAME"
    docker exec -it $CONTAINER_NAME /bin/bash
}

function Invoke-Cleanup {
    Write-Host "Cleaning up container and image..."
    Stop-Container
    docker rmi "$IMAGE_NAME`:$TAG" 2>$null
    Write-Host "Cleanup complete!" -ForegroundColor Green
}

# Main script logic
switch ($Command) {
    "build" { Invoke-Build }
    "run" { Start-Container }
    "stop" { Stop-Container }
    "logs" { Show-Logs }
    "shell" { Open-Shell }
    "clean" { Invoke-Cleanup }
    default { Show-Usage }
}
