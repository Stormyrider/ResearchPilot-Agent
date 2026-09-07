# ResearchPilot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/LangChain-Agent-1C3C3C?logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-F97316" alt="LangGraph">
  <img src="https://img.shields.io/badge/Google%20Gemini-LLM%20%26%20Embeddings-4285F4?logo=googlegemini&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6F00" alt="ChromaDB">
  <img src="https://img.shields.io/badge/Tavily-Web%20Search-6C4EFF" alt="Tavily">
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/SQLite-Persistence-07405E?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-In%20Development-yellow" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

> An agentic research assistant that combines private knowledge, live web research, and evidence-based report generation.

ResearchPilot is an agentic research assistant built with **Google Gemini, LangChain, and LangGraph**. It searches a private knowledge base using RAG, performs live web research through Tavily, combines internal and external evidence, maintains conversation state and memory, generates Markdown reports, and records research interactions.

The system follows one guiding principle:

> **Use trusted evidence when available, clearly distinguish internal and external sources, and never claim an action succeeded when it failed.**

---

## Table of Contents

* [Overview](#overview)
* [Core Architecture](#core-architecture)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [How ResearchPilot Works](#how-researchpilot-works)
* [RAG Pipeline](#rag-pipeline)
* [Agent Workflow](#agent-workflow)
* [Memory and State](#memory-and-state)
* [Source Handling](#source-handling)
* [Guardrails and Reliability](#guardrails-and-reliability)
* [Observability](#observability)
* [Database](#database)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Run Locally](#run-locally)
* [Example Requests](#example-requests)
* [End-to-End Test](#end-to-end-test)
* [Streamlit](#streamlit)
* [Deployment](#deployment)
* [Security](#security)
* [Current Status](#current-status)
* [Future Improvements](#future-improvements)
* [Project Summary](#project-summary)

---

## Overview

ResearchPilot receives a natural-language research request and uses a Gemini-powered agent to decide what actions are required.

The main research tools are:

| Tool | Purpose |
|---|---|
| **Web Search** | Tavily for current and external information |
| **RAG Search** | Chroma-backed retrieval from the private knowledge base |
| **Save Report** | Saves completed research as a Markdown file |

The agent can call one or more tools, observe their results, update its state, and continue until it has enough information to produce a final response.

For a complex request, the flow looks like this:

```text
User Request
     ↓
Gemini Agent
     ↓
RAG Search
     ↓
Observation
     ↓
Agent State
     ↓
Gemini Agent
     ↓
Web Search
     ↓
Observation
     ↓
Agent State
     ↓
Gemini Agent
     ↓
Save Report
     ↓
Observation
     ↓
Final Response
```

---

## Core Architecture

```text
                         RESEARCHPILOT
                              │
                              ▼
                        Gemini Agent
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              Web Search     RAG       Save Report
                 │            │            │
               Tavily       Chroma        File
                 │            │
                 └────────────┼────────────┘
                              ▼
                         Agent State
                              │
                              ▼
                       Final Response
```

Supporting capabilities strengthen the same architecture:

```text
                    ┌────────────────────┐
                    │     Guardrails      │
                    └─────────┬──────────┘
                              │
                              ▼
User → Gemini Agent → Tools → Agent State → Final Response
                          │        │
                          │        ├── Short-term memory
                          │        ├── Long-term memory
                          │        └── Database
                          │
                          ├── Controlled retries
                          └── Source handling

                    LangSmith → Observability
```

---

## Features

### Agent and Orchestration
- Google Gemini as the primary reasoning model
- LangChain Agent
- LangGraph underneath the agent
- Function/tool calling
- Multi-step tool chaining
- Stateful execution
- Evidence-driven final responses

### Research
- PDF loading
- Recursive text chunking
- Gemini embeddings
- Chroma vector database
- Private semantic retrieval
- Tavily live web search
- Combined RAG + web research
- Source-aware research

### Memory
- Short-term memory between turns
- Long-term memory for remembered user information
- Session/thread separation

### Reliability
- Basic input validation
- Prompt-injection guardrails
- Secret protection
- Controlled tool retries
- Graceful tool errors
- API error handling

### Output
- Markdown report generation
- Report storage in `reports/`
- Source information preservation
- Database logging

### Observability
- LangSmith tracing
- Agent/tool execution visibility
- Error tracing

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini |
| Agent Framework | LangChain |
| Orchestration | LangGraph |
| Web Search | Tavily |
| Embeddings | Gemini Embeddings |
| Vector Store | ChromaDB |
| PDF Processing | PyPDF |
| Text Splitting | RecursiveCharacterTextSplitter |
| Memory | LangGraph state/store |
| Observability | LangSmith |
| Database | SQLite |
| Reports | Markdown |
| UI | Streamlit / Custom UI |
| Version Control | Git / GitHub |

---

## Project Structure

The project intentionally keeps the codebase small.

```text
ResearchPilot/
│
├── agent.py
├── tools.py
├── knowledge.py
│
├── documents/
│   └── ResearchPilot_Sample_Knowledge_Base.pdf
│
├── reports/
│
├── chroma_db/
│
├── researchpilot.db
│
├── .env
├── requirements.txt
└── README.md
```

### File Responsibilities

**`agent.py`** — Main orchestration layer containing:
- Gemini model
- LangChain Agent
- LangGraph state
- Short-term memory
- Long-term memory
- Guardrails
- Controlled retries
- LangSmith tracing
- Database logging
- Application entry point

**`tools.py`** — Contains the core tools:
```text
search_private_knowledge()
search_web()
save_report()
```

**`knowledge.py`** — Contains the private knowledge pipeline:
```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Gemini Embeddings
 ↓
Chroma
 ↓
Semantic Retrieval
```

---

## How ResearchPilot Works

**1. User Request** — The user enters a natural-language research goal, e.g.:
```text
Explain how ResearchPilot combines internal knowledge
with current web research.
```

**2. Gemini Agent** — Gemini interprets the request and decides whether it needs:
```text
Private information → RAG
Current information → Web
Both → RAG + Web
Report → Save Report
```

**3. Tool Execution** — The selected tool executes the requested action.

**4. Observation** — The tool result is returned to the agent.

**5. State Update** — The result becomes part of the agent's current research state.

**6. More Work or Final Answer** — The agent decides:
```text
More work required?
    ├── YES → another tool
    └── NO  → final response
```

---

## RAG Pipeline

The private knowledge pipeline:

```text
PDF
 ↓
PyPDF
 ↓
Pages
 ↓
RecursiveCharacterTextSplitter
 ↓
Chunks
 ↓
Gemini Embeddings
 ↓
Chroma
 ↓
Similarity Search
 ↓
Relevant Internal Evidence
```

A semantic query follows:

```text
User Query
    ↓
Gemini Query Embedding
    ↓
Chroma Similarity Search
    ↓
Top Relevant Chunks
    ↓
Source Metadata
```

The sample ResearchPilot knowledge base contains internal information such as:
- NovaTech AI Lab
- ResearchPilot
- Project code `NP-01`
- Chroma
- LangGraph
- Gemini
- Report storage
- Source selection rules
- Safety rules

---

## Agent Workflow

### Private Question
```text
User
 ↓
Gemini Agent
 ↓
search_private_knowledge
 ↓
Chroma
 ↓
Observation
 ↓
Final Response
```

### Current External Question
```text
User
 ↓
Gemini Agent
 ↓
search_web
 ↓
Tavily
 ↓
Observation
 ↓
Final Response
```

### Combined Research
```text
User
 ↓
Gemini Agent
 ↓
RAG Search
 ↓
Observation
 ↓
Gemini Agent
 ↓
Web Search
 ↓
Observation
 ↓
Gemini Agent
 ↓
Save Report
 ↓
Observation
 ↓
Final Response
```

---

## Memory and State

ResearchPilot has two memory concepts.

### Short-Term Memory

Keeps the current conversation associated with a LangGraph thread:

```text
Thread ID
    ↓
Conversation State
    ↓
Turn 1
    ↓
Turn 2
    ↓
Turn 3
```

Example:
```text
User: What is ResearchPilot?
User: What is its project code?
```
The second request can use the previous conversation to understand `its`.

### Long-Term Memory

Stores information explicitly requested to be remembered:

```text
User ID
    ↓
Long-Term Memory
    ↓
Future Conversations
```

Example:
```text
User: Remember that I prefer Python examples.
Later: Use my preferred language.
```
The long-term-memory layer can retrieve the stored information.

---

## Source Handling

ResearchPilot distinguishes between internal and external evidence.

**Internal:**
```text
[INTERNAL SOURCE]
File: ResearchPilot_Sample_Knowledge_Base.pdf
Page: 1
```

**External:**
```text
[EXTERNAL SOURCE]
Title: Example article
URL: https://example.com
```

The final response keeps these source types separate. ResearchPilot should **never**:
- Present web information as internal information
- Present internal information as web information
- Invent a source
- Claim evidence exists when the retrieval tool returned nothing

---

## Guardrails and Reliability

### Input Validation
Basic validation prevents empty or obviously invalid requests from being processed.

### Guardrails
The agent protects against simple prompt-injection and secret-disclosure attempts, including attempts to:
```text
Reveal system instructions
Reveal API keys
Ignore protected instructions
Expose hidden prompts
```

### Tool Errors
Tool errors are returned to the agent in a controlled way. Instead of the application crashing, the workflow becomes:

```text
Tool
 ↓
Error
 ↓
Limited Retry
 ↓
Still failing?
 ↓
Controlled Tool Error
 ↓
Agent decides what to do
```

### Controlled Retries
Transient problems such as:
```text
429
503
timeout
connection failure
network failure
```
can be retried a limited number of times. Persistent failures are surfaced instead of being incorrectly reported as successful.

---

## Observability

ResearchPilot uses **LangSmith** for tracing. Execution can be viewed as:

```text
User Request
     ↓
Gemini Agent
     ↓
Tool Selection
     ↓
Tool Input
     ↓
Tool Output
     ↓
Next Agent Step
     ↓
Final Response
```

Example configuration:
```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=ResearchPilot
```

> ⚠️ Never commit the LangSmith API key to Git.

---

## Database

ResearchPilot records application interactions in SQLite.

**Database:** `researchpilot.db`
**Primary table:** `conversations`

Stored information includes:
```text
id
user_id
thread_id
question
answer
created_at
```

The database acts as a persistence/logging layer and does not replace Chroma or the agent state.

---

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY>
cd ResearchPilot
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=ResearchPilot
```

> ⚠️ Never commit `.env`.

Recommended `.gitignore`:
```text
.env
venv/
__pycache__/
chroma_db/
*.db
```

---

## Run Locally

Activate the environment (see [Installation](#installation)), then run the agent:

```bash
python agent.py
```

Expected startup:
```text
ResearchPilot
Type 'exit' to quit.
```

Enter a request:
```text
What is ResearchPilot?
```

---

## Example Requests

### Private Knowledge
```text
What is the ResearchPilot project code?
```
Expected tool: `search_private_knowledge`

### Current Research
```text
What are the latest developments in RAG?
```
Expected tool: `search_web`

### Combined Research
```text
Compare the latest developments in RAG
with ResearchPilot's internal RAG architecture.
```
Expected behavior:
```text
RAG → Web → Synthesis → Final Response
```

### Report Generation
```text
Research the latest developments in RAG,
compare them with ResearchPilot's internal
knowledge, and save a short report.
```
Expected behavior:
```text
RAG → Web → Save Report → Final Response
```

---

## End-to-End Test

A full workflow test should use:
```text
Research the latest developments in RAG,
compare them with ResearchPilot's internal
knowledge, and save a short report.
```

Expected tool pattern:
```text
[TOOL] search_private_knowledge
[TOOL] search_web
[TOOL] save_report
```

The generated report should appear under `reports/`. This validates the intended `RAG → Web → Save → Final Response` workflow.

---

## Streamlit

Streamlit is the presentation layer for the agent. It should not replace the ResearchPilot backend.

```text
Browser
   ↓
Streamlit UI
   ↓
ResearchPilot Agent
   ↓
Gemini + LangGraph
   ↓
Tools
   ↓
Agent State
   ↓
Final Response
```

A future custom UI created with another frontend tool can also be connected through the same backend without changing the core ResearchPilot architecture.

---

## Deployment

The intended lightweight deployment path:

```text
Local Project
     ↓
GitHub
     ↓
Streamlit Community Cloud
     ↓
Secrets / Environment Variables
     ↓
Live ResearchPilot
```

Before deployment, confirm:
- [ ] `requirements.txt` is up to date
- [ ] `streamlit_app.py` is present
- [ ] `.env` is excluded from Git
- [ ] API keys are stored as deployment secrets

For production use, persistent storage should also be considered for memory and database records, since in-memory stores are primarily suitable for development/testing.

---

## Security

**Protect API Keys** — Never commit:
```text
GEMINI_API_KEY
TAVILY_API_KEY
LANGSMITH_API_KEY
```

**Restrict Report Writing** — The report tool should write only inside `reports/`.

**Do Not Expose Unrestricted Execution** — ResearchPilot should not provide unrestricted shell execution or arbitrary file deletion.

**Treat External Content as Untrusted** — Web pages and retrieved documents are evidence, not system instructions.

---

## Current Status

### Completed Core System
```text
✅ Gemini
✅ LangChain Agent
✅ LangGraph
✅ Tool Calling
✅ Web Search
✅ PDF Loading
✅ Chunking
✅ Gemini Embeddings
✅ Chroma
✅ Private Knowledge Retrieval
✅ RAG + Web Combination
✅ Multi-Step Tool Chaining
✅ Report Generation
✅ Basic Retries
✅ Basic Input Validation
✅ Short-Term Memory
✅ Long-Term Memory
✅ Better Guardrails
✅ Controlled Tool Error Handling
✅ Observability / LangSmith
✅ Better Source Handling
✅ Database Action
✅ Final Architecture Cleanup
```

### Remaining Delivery Work
```text
⬜ Final architecture diagram asset
⬜ Custom UI
⬜ Streamlit integration
⬜ Deployment
```

---

## Future Improvements

### Date-Aware Web Search

Research requests containing words like `latest`, `today`, `recent`, `current`, `this week` can be improved by making the search query explicitly date-aware — for example, `latest developments in RAG 2026` rather than allowing old-year wording to dominate the search.

### Retrieval Improvements

Possible future enhancements include:
- Hybrid keyword + vector search
- Reranking
- Query rewriting
- Retrieval evaluation
- Richer source citations
- Improved document parsing
- Multimodal document support

These are optional enhancements beyond the current ResearchPilot architecture.

---

## Project Summary

ResearchPilot combines:

```text
Google Gemini
      +
LangChain
      +
LangGraph
      +
RAG / Chroma
      +
Tavily
      +
Memory
      +
Guardrails
      +
Retries
      +
LangSmith
      +
SQLite
      +
Report Generation
```

to create an evidence-oriented agent capable of researching across **private organizational knowledge and live external sources**.

The result is a modular research system where the **Gemini agent decides**, the **tools execute**, **state preserves context**, and the **final response is grounded in gathered evidence**.
