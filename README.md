# YouTube Transcript API

A FastAPI-based REST API for fetching YouTube video transcripts with Azure Key Vault integration for secure API key management.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **YouTube Transcript API**: Fetch transcripts from YouTube videos
- **Azure Key Vault Integration**: Secure API key management
- **Docker Support**: Containerized deployment
- **AKS Ready**: Kubernetes deployment manifests included
- **Multiple Language Support**: Request transcripts in specific languages
- **Flexible Configuration**: Environment variables, Key Vault, or local settings file

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with API key status

### Transcript
- `POST /transcript/{video_id}` - Get transcript by video ID with optional language parameter

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   cd "{PythonFastAPI}"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

### Docker

1. **Build the image**:
   ```bash
   docker build -t youtube-transcript-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 -e AZURE_KEY_VAULT_URL="https://your-keyvault.vault.azure.net/" youtube-transcript-api
   ```

## Configuration Priority

The application loads the YouTube API key in the following order:

1. **Azure Key Vault** (if `AZURE_KEY_VAULT_URL` is set)
2. **Environment Variable** (`YOUTUBE_API_KEY`)
3. **Local Settings File** (`settings.json`)



### Azure Key Vault Setup

1. **Create a Key Vault** in Azure
2. **Add the API key** as a secret named `YouTubeApiKey`
3. **Configure authentication**:
   - For AKS: Use Workload Identity (recommended)
   - For local development: Use Azure CLI (`az login`)
   - For other scenarios: Set `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`

## API Usage Examples


### Response Format


## Deployment to AKS

### Prerequisites
- Azure Container Registry (ACR)
- Azure Kubernetes Service (AKS)
- Azure Key Vault
- Workload Identity enabled on AKS

### Steps

1. **Build and push to ACR**:
   ```bash
   az acr build --registry your-registry --image youtube-transcript-api:latest .
   ```

2. **Update Kubernetes manifests**:
   - Edit `k8s-deployment.yaml`
   - Replace placeholders with your values
   - Configure managed identity client ID

3. **Deploy to AKS**:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

4. **Configure Key Vault access**:
   ```bash
   # Create managed identity
   az identity create --name youtube-transcript-identity --resource-group your-rg
   
   # Grant Key Vault access
   az keyvault set-policy --name your-keyvault --object-id <identity-object-id> --secret-permissions get
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_KEY_VAULT_URL` | Azure Key Vault URL | No |
| `YOUTUBE_API_KEY` | YouTube API key (fallback) | No |
| `PORT` | Server port (default: 8000) | No |
| `AZURE_CLIENT_ID` | Azure service principal client ID | No* |
| `AZURE_CLIENT_SECRET` | Azure service principal secret | No* |
| `AZURE_TENANT_ID` | Azure tenant ID | No* |

*Required only if not using managed identity

## Security Features

- Non-root container user
- Health checks for Kubernetes
- Resource limits
- CORS middleware
- Secure secret management
- No hardcoded credentials

## API Documentation

Once running, visit:
- Interactive docs: `http://localhost:8000/docs`
- OpenAPI spec: `http://localhost:8000/openapi.json`

## Troubleshooting

### Common Issues

1. **No API key found**: Check configuration priority and ensure at least one source is configured
2. **Key Vault access denied**: Verify managed identity permissions
3. **Video not found**: Ensure video ID is correct and video has transcripts available
4. **Language not available**: Try without specifying languages or check available languages

### Logs

The application uses structured logging. Check container logs:
```bash
kubectl logs -f deployment/PythonFastAPI
```

## License

This project is provided as-is for educational and development purposes.
