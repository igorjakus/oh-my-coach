# Oh My Coach
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
1. Install UV package manager:
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

## Development resources
[Database diagrams](https://dbdiagram.io/)
[Full-Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)
[Hackathon-Starter](https://github.com/Kabanosk/hackathon-starter/) - this repo is heavily inspired by this:)
[Hackathon-Booster](https://github.com/igorjakus/hackathon-booster/)
