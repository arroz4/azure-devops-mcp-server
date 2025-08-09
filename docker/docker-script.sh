#!/bin/bash

# Docker build and run script for ADO MCP Server

set -e

IMAGE_NAME="ado-mcp-server"
TAG="latest"
CONTAINER_NAME="ado-mcp-server"
PORT="8000"

# Function to display usage
usage() {
    echo "Usage: $0 [build|run|stop|logs|shell|clean]"
    echo ""
    echo "Commands:"
    echo "  build   - Build the Docker image"
    echo "  run     - Run the container"
    echo "  stop    - Stop and remove the container"
    echo "  logs    - Show container logs"
    echo "  shell   - Open shell in running container"
    echo "  clean   - Remove container and image"
    echo ""
}

# Build Docker image
build() {
    echo "Building Docker image: $IMAGE_NAME:$TAG"
    docker build -f docker/Dockerfile -t $IMAGE_NAME:$TAG .
    echo "Build complete!"
}

# Run container
run() {
    echo "Starting container: $CONTAINER_NAME"
    
    # Stop existing container if running
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        echo "Stopping existing container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    fi
    
    # Run new container
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:$PORT \
        --env-file .env \
        $IMAGE_NAME:$TAG
    
    echo "Container started! Access at http://localhost:$PORT"
    echo "Health check: http://localhost:$PORT/health"
}

# Stop container
stop() {
    echo "Stopping container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    echo "Container stopped and removed!"
}

# Show logs
logs() {
    echo "Showing logs for: $CONTAINER_NAME"
    docker logs -f $CONTAINER_NAME
}

# Open shell
shell() {
    echo "Opening shell in: $CONTAINER_NAME"
    docker exec -it $CONTAINER_NAME /bin/bash
}

# Clean up
clean() {
    echo "Cleaning up container and image..."
    stop
    docker rmi $IMAGE_NAME:$TAG 2>/dev/null || true
    echo "Cleanup complete!"
}

# Main script logic
case "$1" in
    build)
        build
        ;;
    run)
        run
        ;;
    stop)
        stop
        ;;
    logs)
        logs
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    *)
        usage
        exit 1
        ;;
esac
