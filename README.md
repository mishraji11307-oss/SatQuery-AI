# SatQuery AI

An interactive vision-language assistant for exploring and analysing optical, SAR, and multi-temporal satellite imagery. SatQuery AI combines a browser-based workspace with a FastAPI backend for image uploads, analysis, visual evidence, and chat.

> Developed for Smart India Hackathon 2026 - problem statement SIH26167.

## Features

- Single-image remote-sensing question answering
- Visual grounding and region-of-interest analysis
- Bi-temporal change analysis
- Optical and SAR image workflows
- Image metadata inspection and upload management
- Analysis history, health checks, and interactive API documentation
- Demo mode that runs without external model weights

## Project layout

```text
.
|-- api/                 # Serverless API entry point
|-- backend/             # FastAPI application, migrations, and tests
|-- documents/           # Project documentation
|-- frontend/            # Browser-based application
|-- storage/             # Local data and generated files
|-- requirements.txt     # Root/serverless Python dependencies
`-- vercel.json          # Vercel deployment configuration
```

## Run locally

Requirements: Python 3.11 or newer.

### 1. Start the API

In PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API defaults to demo mode and SQLite, so no `.env` file, external database, or model download is needed for a local demo. Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

### 2. Start the frontend

In a second PowerShell window:

```powershell
cd frontend
py -m http.server 5500
```

Open [http://localhost:5500](http://localhost:5500). The frontend uses the API on port 8000 when served on port 5500.

## Run tests

From the repository root:

```powershell
cd backend
python -m pytest tests -v
```

## Docker Compose

The Docker Compose setup starts the backend, PostgreSQL, and Redis. Set unique credentials in the current PowerShell session before starting it:

```powershell
$env:SECRET_KEY = "<a-long-random-secret>"
$env:POSTGRES_PASSWORD = "<a-unique-database-password>"
cd backend
docker compose up --build
```

Do not commit credentials or put real secrets in source files. For deployments, configure secrets and other environment-specific settings through the deployment platform.

## Deployment

The repository includes a Vercel configuration for the frontend and serverless API entry point. Configure deployment secrets in the Vercel project settings; do not rely on development defaults for production.

## License

No license is currently included. All rights remain with the project contributors unless a license is added.
