<!-- 
# Sample Python FastAPI Project Documentation

This document serves as a sample for documenting a Python FastAPI project. It outlines the features, API endpoints, setup instructions, deployment steps, configuration priorities, and troubleshooting tips for a FastAPI-based REST API. The project integrates with Azure Key Vault for secure API key management and supports containerized deployment with Docker and Kubernetes.

## Features

- FastAPI framework for building modern APIs
- Integration with YouTube Transcript API for fetching video transcripts
- Secure API key management using Azure Key Vault
- Docker support for containerized deployment
- Kubernetes deployment manifests for Azure Kubernetes Service (AKS)
- Multiple language support for transcripts
- Flexible configuration options via environment variables, Key Vault, or local settings

## API Endpoints

### Health Check
- `GET /`: Basic health check
- `GET /health`: Detailed health check with API key status

### Transcript
- `POST /transcript/{video_id}`: Fetch transcript by video ID with optional language parameter

## Quick Start

### Local Development
1. Clone the repository and navigate to the project directory.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure environment variables by copying `.env.example` to `.env` and editing the settings.
4. Run the application locally using `python main.py`.

### Docker Deployment
1. Build the Docker image using `docker build -t youtube-transcript-api .`.
2. Run the container with environment variables using `docker run -p 8000:8000 -e AZURE_KEY_VAULT_URL="https://your-keyvault.vault.azure.net/" youtube-transcript-api`.

## Configuration Priority

The application loads the YouTube API key in the following order:
1. Azure Key Vault (if `AZURE_KEY_VAULT_URL` is set)
2. Environment Variable (`YOUTUBE_API_KEY`)
3. Local Settings File (`settings.json`)

## Azure Key Vault Setup

1. Create a Key Vault in Azure and add the API key as a secret named `YouTubeApiKey`.
2. Configure authentication using Workload Identity for AKS or Azure CLI for local development.
3. Set required environment variables for other scenarios.

## Deployment to AKS

### Prerequisites
- Azure Container Registry (ACR)
- Azure Kubernetes Service (AKS)
- Azure Key Vault
- Workload Identity enabled on AKS

### Steps
1. Build and push the Docker image to ACR using `az acr build`.
2. Update Kubernetes manifests with your values and deploy using `kubectl apply`.
3. Configure Key Vault access for the managed identity.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_KEY_VAULT_URL` | Azure Key Vault URL | No |
| `YOUTUBE_API_KEY` | YouTube API key (fallback) | No |
| `PORT` | Server port (default: 8000) | No |
| `AZURE_CLIENT_ID` | Azure service principal client ID | No* |
| `AZURE_CLIENT_SECRET` | Azure service principal secret | No* |
| `AZURE_TENANT_ID` | Azure tenant ID | No* |

*Required only if not using managed identity.

## Security Features

- Non-root container user
- Health checks for Kubernetes
- Resource limits
- CORS middleware
- Secure secret management
- No hardcoded credentials

## API Documentation

Interactive API documentation is available at:
- `http://localhost:8000/docs` for Swagger UI
- `http://localhost:8000/openapi.json` for OpenAPI specification

## Troubleshooting

### Common Issues
1. Missing API key: Ensure configuration priority is followed.
2. Key Vault access denied: Verify managed identity permissions.
3. Video not found: Check video ID and transcript availability.
4. Language not available: Retry without specifying a language.

### Logs
Structured logging is enabled. Check container logs using:
