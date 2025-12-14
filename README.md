# 🛡️ NeuralAudit: AI Reliability & Compliance Engine

**NeuralAudit** is an automated evaluation pipeline designed to audit RAG (Retrieval-Augmented Generation) chatbots. It assesses AI responses against "Ground Truth" context vectors to detect **Hallucinations**, measure **Relevance**, and calculate **Cost/Latency** metrics in real-time.

![NeuralAudit Dashboard](static/dashboard.png)

## 📋 Project Overview

In the era of Generative AI, reliability is the biggest bottleneck. NeuralAudit acts as a "Judge" that sits between the User and the AI, ensuring compliance and accuracy.

The system takes two inputs:
1.  **Chat Log (JSON):** The conversation history between the user and the bot.
2.  **Context Vector (JSON):** The actual source data retrieved from the vector database.

It then uses a **Dual-Layer Evaluation System** to grade the interaction:
* **Deterministic Layer:** Calculates Token Usage, Latency, and Cost ($).
* **Probabilistic Layer (LLM Judge):** Uses **Google Gemini 2.5 Flash** to semantically grade the response for "Relevance" and "Factual Accuracy."

## 🚀 Key Features

* **Cyber-Core Dashboard:** A responsive, glassmorphism-based UI for real-time monitoring.
* **Hallucination Detection:** Rigorous cross-referencing of AI claims vs. Context source material.
* **Relevance Scoring:** Determines if the AI actually answered the user's specific intent.
* **Performance Metrics:** Tracks latency (ms) and estimated cost per interaction.
* **Visualizations:** Radar charts for at-a-glance reliability indexing.

## 🏗️ Technical Architecture

The system follows a modular **Microservice-Lite** architecture:

1.  **Frontend (Cyber Core):**
    * Built with **HTML5, CSS3 (Neon/Glass UI), and JavaScript**.
    * Uses **Chart.js** for real-time data visualization.
2.  **API Server (FastAPI):**
    * High-performance Python backend handling asynchronous requests.
    * Serves static assets and processes JSON uploads.
3.  **Evaluation Engine (`src/`):**
    * **Ingestion:** Parses complex nested JSONs and cleans "dirty" data (comments/trailing commas).
    * **Judge Agent:** Leverages **LangChain** and **Google Gemini 2.5** for reasoning.
    * **Metrics:** Uses `tiktoken` for precise token counting and cost estimation.

### 🛠️ Tech Stack
* **Language:** Python 3.11
* **Backend Framework:** FastAPI + Uvicorn
* **LLM Orchestration:** LangChain
* **Model:** Google Gemini 2.5 Flash
* **Frontend:** Vanilla JS + Chart.js

## 📂 Project Structure

```text
NeuralAudit/
│
├── api.py                   # Main FastAPI Server entry point
├── requirements.txt         # Project dependencies
├── .env                     # API Keys (Not uploaded to Git)
│
├── static/                  # Frontend Assets
│   ├── index.html           # Dashboard UI
│   ├── style.css            # Cyberpunk Styling
│   ├── script.js            # Client-side Logic
│   └── dashboard.png        # Screenshot for README
│
└── src/                     # Core Logic Modules
    ├── ingestion.py         # JSON Parsing & Cleaning
    ├── metrics.py           # Cost & Latency Math
    └── judge.py             # LLM Evaluation Prompts

⚡ Scalability Strategy (Scaling to Millions)
To scale NeuralAudit from this prototype to handling millions of daily conversations, the following architecture changes are proposed:

Async Queueing: Replace direct API calls with a message queue (RabbitMQ or Kafka). Evaluation requests would be pushed to a queue and processed by a distributed fleet of worker nodes.

Semantic Caching (Redis): Before calling the LLM Judge, check a Redis Vector Cache. If a similar Query+Context has been evaluated before, return the cached score. This reduces API costs by ~40%.

Tiered Evaluation:

Tier 1 (Regex/Heuristics): Instant check for formatting errors (Cost: $0).

Tier 2 (Small Model): Use a quantized local model (e.g., Llama-3-8B) for standard checks.

Tier 3 (Gemini/GPT-4): Only used for complex reasoning or disputes.

⚙️ Setup & Installation
1. Clone the repository

Bash

git clone [https://github.com/your-username/NeuralAudit.git](https://github.com/your-username/NeuralAudit.git)
cd NeuralAudit
2. Install dependencies

Bash

pip install -r requirements.txt
3. Set up Environment Variables Create a .env file in the root directory and add your Google Gemini API key:

Plaintext

GOOGLE_API_KEY=your_api_key_here
▶️ How to Run
Start the Server: Run the following command in your terminal:

Bash

uvicorn api:app --reload
Access the Dashboard: Open your browser and navigate to: http://127.0.0.1:8000

Run an Audit:

Upload a Chat Log JSON.

Upload a Context Vector JSON.

Click "INITIATE AUDIT SEQUENCE".