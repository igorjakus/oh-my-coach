# Oh My Coach
Agentic AI coach that helps you crush your goals — and go beyond!

---

## Table of Contents
1. [Setup](#setup)
   - [Environment Setup](#environment-setup)
   - [Install UV Package Manager](#install-uv-package-manager)
   - [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
   - [Create Database](#create-database)
2. [Development Resources & Acknowledgments](#development-resources--acknowledgments)

---

## Setup

### Environment Setup
Create a `.env` file in the root directory of the project. 
This file will store your configuration and API keys. 
See `.env.example` for an example.

> **Note:** Never commit your `.env` file to version control. The `.gitignore` file already includes it.

### Install UV Package Manager
Install the UV package manager by running the following command:

```bash
pip install uv
```

### Create and Activate Virtual Environment
Synchronize dependencies and activate the virtual environment:

```bash
uv sync
source .venv/bin/activate
```

### Create Database
Run the following commands to create a database and user:

```bash
psql postgres -c "CREATE USER hackathon WITH PASSWORD 'hackathon';" && \
psql postgres -c "CREATE DATABASE hackathon OWNER hackathon;"
```

**Database Structure**
![Database Structure](docs/database-design.png)

### Run backend
```bash
fastapi dev backend/main.py
```
You can see endpoints going to adress `http://localhost:8000/docs` in your favorite browser:)

---

## Development Resources & Acknowledgments
- [Database diagrams](https://dbdiagram.io/)
- [Full-Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)
- [Hackathon-Starter](https://github.com/Kabanosk/hackathon-starter/) - this repo is heavily inspired by this :)
- [Hackathon-Booster](https://github.com/igorjakus/hackathon-booster/)
- [OpenAI-Realtime-FastAPI](https://github.com/Geo-Joy/openai-realtime-fastapi)

---
