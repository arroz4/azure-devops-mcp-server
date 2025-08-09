# Docker Setup for ADO MCP Server

This folder contains all Docker-related files for the Azure DevOps MCP Server.

## Files

- **`Dockerfile`** - Main Docker image definition
- **`.dockerignore`** - Files to exclude from Docker build context
- **`docker-compose.yml`** - Development environment setup
- **`docker-compose.prod.yml`** - Production environment with resource limits
- **`docker-script.ps1`** - PowerShell helper script for Windows
- **`docker-script.sh`** - Bash helper script for Linux/Mac

## Quick Start

### Using Docker Scripts

**From the project root directory:**

**Windows (PowerShell):**
```powershell
.\docker\docker-script.ps1 build    # Build image
.\docker\docker-script.ps1 run      # Run container
.\docker\docker-script.ps1 logs     # View logs
.\docker\docker-script.ps1 stop     # Stop container
```

**Linux/Mac (Bash):**
```bash
./docker/docker-script.sh build    # Build image
./docker/docker-script.sh run      # Run container
./docker/docker-script.sh logs     # View logs
./docker/docker-script.sh stop     # Stop container
```

### Using Docker Compose

**From the project root directory:**

```bash
# Development
docker-compose -f docker/docker-compose.yml up -d

# Production
docker-compose -f docker/docker-compose.prod.yml up -d
```

### Using Docker Directly

**From the project root directory:**

```bash
# Build
docker build -f docker/Dockerfile -t ado-mcp-server .

# Run
docker run -d --name ado-mcp-server -p 8000:8000 --env-file .env ado-mcp-server
```

## Environment Variables

Ensure your `.env` file in the project root contains:

```env
AZURE_DEVOPS_PAT=your_personal_access_token
AZURE_DEVOPS_PROJECT=your_project_name
AZURE_DEVOPS_ORGANIZATION_URL=https://dev.azure.com/your_organization
MCP_SERVER_PORT=8000
```

## Health Check

Once running, verify the service is accessible:

```bash
# Check if server is running on the MCP endpoint
curl http://localhost:8000/mcp/
```

## Notes

- All Docker commands should be run from the **project root directory**, not from this docker folder
- The Dockerfile builds from the project root context to access all necessary files
- The .dockerignore file excludes development files from the build context
- Scripts automatically handle container lifecycle management
