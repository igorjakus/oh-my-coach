# OpenAI Hackathon 2025 - Oh My Coach

Agentic AI coach that helps you crush your goals — and go beyond!

## Setup
### Environment Setup
Create a `.env` file in the root directory of the project. This file will store your configuration and API keys.

Example `.env` file:
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key

# Database Configuration (optional - default values shown)
POSTGRES_USER=hackathon
POSTGRES_PASSWORD=hackathon
POSTGRES_DB=hackathon
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Other Settings
DEBUG=true
LOG_LEVEL=INFO
```

Note: Never commit your `.env` file to version control. The `.gitignore` file already includes it.

### Option 1: Local Setup with UV
1. Install UV packagllm jailbreakinge manager:
```bash
pip install uv
```

2. Create and activate virtual environment:
```bash
uv sync
source .venv/bin/activate
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

### Option 2: Docker Setup
1. Build and run with Docker Compose:
```bash
docker compose up
```


## Technologies

## Images

## Project Overview

### Inspiration

### What it does

### How we built it

### Challenges we ran into

### What we learned

### What's next for Oh My Coach

### How to run

