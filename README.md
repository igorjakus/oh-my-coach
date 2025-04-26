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
## Description

The application offers a personal agent who acts as both a supportive friend and a dedicated coach. It gets to know you over time, helps you stay motivated, assists in organizing your daily plans, and supports you in achieving your goals. At the end of the day, it also provides a space to clear your mind and reflect before sleep.

## Technologies

## Images

## Project Overview

### Inspiration

Some people live busy lives and often find themselves at the end of the day with a cluttered mind. The idea behind **Oh-My-Coach** was to provide an app where you could reflect on the events of the day, talk about your goals, worries, and anything you might usually share only with a close friend. When needed, the app enables a retrospective chat that helps you organize your thoughts and find peace of mind.

### What it does?

**Oh-My-Coach** is an AI agent that gradually gets to know you through regular conversations.

When prompted, it consults with a specialist in a relevant field (e.g., dietitian, psychologist, personal trainer), providing them with the full context.

These specialists can see your goals and track your progress. They generate a tailored response and propose a task, which you can choose to accept and add to your personal task list.

The app includes a **Goals and Tasks** view, where you can track your current goals and review the tasks suggested to help you reach them.

Need to clear your head? The **Retro** view allows you to talk to your agent using speech-to-speech, letting you unload your deepest thoughts in a safe space.

### How we built it

- **Python** for backend and **???** for frontend.

### Challenges We Ran Into

**User Simplicity**: Balancing a clean, user-friendly interface with the depth of features we wanted to include was a significant design challenge.

**Custom Prompting**: Crafting precise and effective prompts was essential for guiding the AI to produce meaningful and context-aware responses.

### What We Learned

**New Technologies**: We gained hands-on experience with OpenAI’s Responses API and the new Agent SDK, which were central to building our app’s intelligence.

**Collaboration**: Strong teamwork and clear communication helped us overcome technical and creative challenges throughout the project.

### What's next for Oh My Coach

**Google Calendar Integration**: Automatically sync your tasks with Google Calendar to keep your schedule organized and stay on track.

**Learning Dashboard**: A dedicated space where users can explore curated learning materials tailored to their goals and interests.

### How to run

