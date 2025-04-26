# Oh My Coach

## Table of Contents

* [Oh My Coach](#oh-my-coach)
    * [Table of Contents](#table-of-contents)
    * [Description](#description)
    * [Technologies](#technologies)
    * [Images](#images)
    * [Project Overview](#project-overview)
        * [Inspiration](#inspiration)
        * [What it does?](#what-it-does)
        * [How we built it](#how-we-built-it)
        * [Challenges We Ran Into](#challenges-we-ran-into)
        * [What We Learned](#what-we-learned)
        * [What's next for Oh My Coach](#whats-next-for-oh-my-coach)
    * [Setup](#setup)
        * [Environment Setup](#environment-setup)
        * [Install UV Package Manager](#install-uv-package-manager)
        * [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
        * [Create Database](#create-database)
    * [How to run](#how-to-run)
        * [Run backend](#run-backend)
    * [Agent Pipeline](#agent-pipeline)
        * [Overview Flow](#overview-flow)
        * [Agent Types Hierarchy](#agent-types-hierarchy)
    * [Development Resources & Acknowledgments](#development-resources--acknowledgments)

---

## Description

Oh My Coach! Your simple personal assistant for difficult planning. Just set your goal and let be guided by individual chats, personalized tasks and daily retro recaps.

## Technologies

* Python with FastAPI
* WebRTC and node.js for VTV
* Vanilla HTML + Bootstrap
* OpenAI API
* postgresql

## Images

![Chat](public/images/Screenshot_2025-04-26_at_15.35.43.png)

TBA

## Project Overview

### Inspiration

Some people live busy lives and often find themselves at the end of the day with a cluttered mind. The idea behind **Oh My Coach** was to provide an app where you could reflect on the events of the day, talk about your goals, worries, and anything you might usually share only with a close friend. When needed, the app enables a retrospective chat that helps you organize your thoughts and find peace of mind.

### What it does?

**Oh My Coach** is a multimodal AI agent that gradually gets to know you through regular conversations.

When prompted, triage agent decides which specialists (AI agents) are the most relevant (e.g., nutritionist, psychologist, personal trainer), providing them with the full context.

These specialists can see your goals and track your progress. They generate a tailored response and propose a task, which you can choose to accept and add to your personal task list.

The app includes a **Goals and Tasks** view, where you can track your current goals and review the tasks suggested to help you reach them.

Need to clear your head? The **Retro** view allows you to talk to your OpenAI speech-to-speech agent, letting you unload your deepest thoughts in a safe space.

### How we built it

* **Python** for backend and **???** for frontend.

### Challenges We Ran Into

**User Simplicity**: Balancing a clean, user-friendly interface with the depth of features we wanted to include was a significant design challenge.

**Custom Prompting**: Crafting precise and effective prompts was essential for guiding the AI to produce meaningful and context-aware responses.

### What We Learned

**New Technologies**: We gained hands-on experience with OpenAI’s Responses API and the new Agent SDK, which were central to building our app’s intelligence.

**Collaboration**: Strong teamwork and clear communication helped us overcome technical and creative challenges throughout the project.

### What's next for Oh My Coach

**Google Calendar Integration**: Automatically sync your tasks with Google Calendar to keep your schedule organized and stay on track.

**Learning Dashboard**: A dedicated space where users can explore curated learning materials tailored to their goals and interests.

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

## How to run

### Run backend

```bash
fastapi dev backend/main.py
```
You can see endpoints going to adress `http://localhost:8000/docs` in your favorite browser:)

**We have a lot of endpoints;)**
![API Endpoints](docs/endpoints.png)

---

### Run VTV Node server for voice enabled AI integration

```
# Requries node == 19.0
cd vtv-node-service
npm install
node server.js
```

# Agent Pipeline

## Overview Flow

```mermaid
graph TD
    %% Main Flow Elements
    User([👤 User Input]) --> Session[Session Context]
    Session --> Triage[🎯 Triage Agent]

    %% Intent Classification with confidence scores
    Triage --> IntentCheck{Intent Classification<br/>confidence: 0.0-1.0}
    IntentCheck -->|Task Intent 0.8+| TaskCreation[Task Creation]
    IntentCheck -->|Goal Intent 0.8+| GoalCreation[Goal Creation]
    IntentCheck -->|Chat Intent| AgentSelection[Agent Router]

    %% Task Creation Flow
    TaskCreation --> TaskManager[⚙️ Task Manager Agent]
    TaskManager --> TaskValidation{Validation}
    TaskValidation -->|Valid| DB[(Database)]
    TaskValidation -->|Invalid| TaskCreation

    %% Goal Creation Flow
    GoalCreation --> GoalManager[🎯 Goal Manager Agent]
    GoalManager --> GoalValidation{Validation}
    GoalValidation -->|Valid| DB
    GoalValidation -->|Invalid| GoalCreation
    GoalManager --> InitialTask[Initial Task Generation]
    InitialTask --> TaskManager

    %% Agent Selection Flow with Categories
    AgentSelection --> HealthAgents{Health & Fitness}
    AgentSelection --> MentalAgents{Mental Health}
    AgentSelection --> SupportAgents{Support}
    AgentSelection --> LifestyleAgents{Lifestyle}

    %% Health & Fitness Category
    HealthAgents --> |Physical Health| Physiotherapist[👨‍⚕️ Physiotherapist]
    HealthAgents --> |Exercise Plans| Trainer[💪 Trainer]
    HealthAgents --> |Nutrition| Nutritionist[🥗 Nutritionist]

    %% Mental Health Category
    MentalAgents --> |Mental Health| Psychotherapist[🧠 Psychotherapist]
    MentalAgents --> |Motivation| Motivator[⭐ Motivator]

    %% Support Category
    SupportAgents --> |Friendly Chat| Friend[👋 Friend]
    SupportAgents --> |Entertainment| Entertainer[🎮 Entertainer]
    SupportAgents --> |General Help| Versatile[🔧 Versatile]

    %% Lifestyle Category
    LifestyleAgents --> |Life Coaching| Coach[🎓 Coach]
    LifestyleAgents --> |Goal Planning| Dreamer[💭 Dreamer]

    %% Special Case - Expert with Tools
    AgentSelection --> |Research Needed| Expert[🔍 Expert Agent]
    Expert --> WebSearch[🌐 Web Search Tool]
    Expert --> Documentation[📚 Documentation]

    %% Response Processing - Fixed syntax
    Physiotherapist & Psychotherapist & Motivator & Trainer & Friend & Coach & Dreamer & Nutritionist & Entertainer & Versatile & Documentation & WebSearch --> ResponseProcessor[Response Processor]

    %% Quality Checks
    ResponseProcessor --> QualityCheck{Quality Gate}
    QualityCheck -->|Pass| Personalization[🎨 Personalization Layer]
    QualityCheck -->|Fail| AgentSelection

    %% Final Response Flow
    Personalization --> FeedbackCheck{User Feedback}
    FeedbackCheck -->|Helpful| Analytics[📊 Analytics]
    FeedbackCheck -->|Not Helpful| Session

    %% Session Memory Update
    Analytics --> Session

    %% Styling
    classDef primary fill:#ff9900,stroke:#333,stroke-width:4px;
    classDef secondary fill:#87CEEB,stroke:#333,stroke-width:2px;
    classDef process fill:#98FB98,stroke:#333,stroke-width:2px;
    classDef storage fill:#DDA0DD,stroke:#333,stroke-width:2px;
    classDef input fill:#FFB6C1,stroke:#333,stroke-width:2px;
    classDef validation fill:#FFE4B5,stroke:#333,stroke-width:2px;
    classDef feedback fill:#E6E6FA,stroke:#333,stroke-width:2px;

    class Triage,TaskManager,GoalManager primary;
    class IntentCheck,AgentSelection,HealthAgents,MentalAgents,SupportAgents,LifestyleAgents secondary;
    class ResponseProcessor,Personalization process;
    class DB storage;
    class User,Session input;
    class TaskValidation,GoalValidation,QualityCheck validation;
    class FeedbackCheck,Analytics feedback;
```

## Agent Types Hierarchy

```mermaid
graph TB
    %% Base Structure
    BaseAgent[🤖 Base Agent<br/>Context Aware] --> Health
    BaseAgent --> Mental
    BaseAgent --> Lifestyle
    BaseAgent --> Support
    BaseAgent --> Special

    %% Health Category with Capabilities
    Health[🏥 Health Agents<br/>Medical Knowledge] --> Physiotherapist[👨‍⚕️ Physiotherapist<br/>Exercise Safety]
    Health --> Trainer[💪 Trainer<br/>Workout Plans]
    Health --> Nutritionist[🥗 Nutritionist<br/>Diet Planning]

    %% Mental Health Category
    Mental[🧠 Mental Health<br/>Psychology] --> Psychotherapist[🎯 Psychotherapist<br/>Mental Support]
    Mental --> Motivator[⭐ Motivator<br/>Encouragement]

    %% Lifestyle Category
    Lifestyle[🌟 Lifestyle<br/>Life Planning] --> Coach[🎓 Coach<br/>General Advice]
    Lifestyle --> Dreamer[💭 Dreamer<br/>Goal Setting]

    %% Support Category
    Support[🤝 Support<br/>General Help] --> Friend[👋 Friend<br/>Conversation]
    Support --> Entertainer[🎮 Entertainer<br/>Fun Activities]
    Support --> Versatile[🔧 Versatile<br/>Fallback Agent]

    %% Special Category with Tools
    Special[⚡ Special Agents<br/>Enhanced Access] --> Expert[🔍 Expert<br/>Web Search]
    Special --> TaskManager[⚙️ Task Manager<br/>Task Creation]
    Special --> GoalManager[🎯 Goal Manager<br/>Goal Setting]

    %% Tools and Integrations
    Expert -..->|Uses| WebTools[🌐 Web Tools]
    TaskManager -..->|Uses| Database[(💾 Database)]
    GoalManager -..->|Uses| Database

    %% Styling
    classDef category fill:#ffeb99,stroke:#333,stroke-width:2px;
    classDef agent fill:#87CEEB,stroke:#333,stroke-width:2px;
    classDef tool fill:#98FB98,stroke:#333,stroke-width:2px;
    classDef storage fill:#DDA0DD,stroke:#333,stroke-width:2px;

    class BaseAgent,Health,Mental,Lifestyle,Support,Special category;
    class Physiotherapist,Trainer,Nutritionist,Psychotherapist,Motivator,Coach,Dreamer,Friend,Entertainer,Versatile,Expert,TaskManager,GoalManager agent;
    class WebTools tool;
    class Database storage;
```


## Development Resources & Acknowledgments

* [Database diagrams](https://dbdiagram.io/)
* [Full-Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)
* [Hackathon-Starter](https://github.com/Kabanosk/hackathon-starter/) - this repo is heavily inspired by this :)
* [Hackathon-Booster](https://github.com/igorjakus/hackathon-booster/)
* [OpenAI-Realtime-FastAPI](https://github.com/Geo-Joy/openai-realtime-fastapi)
* [Katia's github with pinned materials](https://github.com/katia-openai)
* [Nice docs about OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
