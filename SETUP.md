# Project Setup Guide

## Overview
This project provides a production-ready FastAPI application for fetching YouTube video transcripts with Azure Key Vault integration.

## Project Structure
```
Lutron.YouTubeTranscriptAPI/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── k8s-deployment.yaml    # Kubernetes deployment manifests
├── .env.example           # Environment variables template
├── settings.json.example  # Local settings template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── test_api.py           # API testing script
├── run-local.ps1         # Local development script (PowerShell)
├── deploy-azure.ps1      # Azure deployment script
├── build.sh              # Build script (Linux/Mac)
├── build.bat             # Build script (Windows)
└── SETUP.md              # This file
```

## Quick Start (Windows)

### Manual Setup
```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env
# Edit .env with your settings

# Run the application
python main.py
```

## Configuration Options

### Option 1: Environment Variables
Create `.env` file:
```
YOUTUBE_API_KEY=your_youtube_api_key
AZURE_KEY_VAULT_URL=https://your-keyvault.vault.azure.net/
```

### Option 3: Azure Key Vault (Production)
Set only the Key Vault URL:
```
AZURE_KEY_VAULT_URL=https://your-keyvault.vault.azure.net/
```

## Testing the API

### 1. Health Check
```bash
curl http://localhost:8000/api/health
```

### 2. Get Transcript
```bash
# POST request
curl -X POST "http://localhost:8000/api/transcript" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "dQw4w9WgXcQ", "languages": "en"}'
```

### 3. Run Test Script
```powershell
python test_api.py
```

## Docker Deployment

### Build Image
```bash
docker build -t youtube-transcript-api .
```

### Run Container
```bash
# With environment variables
docker run -p 8000:8000 \
  -e AZURE_KEY_VAULT_URL="https://your-keyvault.vault.azure.net/" \
  youtube-transcript-api

# With env file
docker run -p 8000:8000 --env-file .env youtube-transcript-api
```

## Azure Deployment

### Prerequisites
- Azure CLI installed and logged in
- Azure PowerShell module
- Docker installed
- kubectl installed

### Automated Deployment
```powershell
.\deploy-azure.ps1 -ResourceGroupName "rg-youtube-api" -KeyVaultName "kv-youtube-api" -AcrName "acryoutubeapi" -AksClusterName "aks-youtube-api" -YouTubeApiKey "your_api_key"
```

## API Documentation

Once running, access:
- Interactive API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure virtual environment is activated
2. **Port already in use**: Change PORT in .env or stop other services
3. **Key Vault access denied**: Check managed identity permissions
4. **No transcripts available**: Not all videos have transcripts

### Check Logs
```bash
# Local
python main.py

# Docker
docker logs <container_id>

# Kubernetes
kubectl logs -f deployment/youtube-transcript-api
```

## Security Best Practices

1. **Never commit secrets** to git
2. **Use managed identities** in Azure
3. **Enable HTTPS** in production
4. **Limit Key Vault access** to minimum required
5. **Use resource limits** in Kubernetes
6. **Regular security updates** for dependencies