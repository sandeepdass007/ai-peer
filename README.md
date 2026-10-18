# AI Peer

AI Peer is a local-first learning companion. This first prototype provides a simple tutor chat using a local Ollama model.

## Requirements

- macOS 14 Sonoma or later
- Python 3.11 or later
- Ollama for macOS and a downloaded local model

## Run the first prototype

1. Install [Ollama for macOS](https://ollama.com/download/mac).
2. In Terminal, download a starter model:

   ```sh
   ollama pull gemma4:e4b
   ```

3. From the AI Peer project folder, create and activate a Python virtual environment, then install the app dependency:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

4. Start AI Peer:

   ```sh
   streamlit run app.py
   ```

Ollama serves the model locally at `http://localhost:11434`. The app uses that local API and does not send prompts to a cloud model. The model download and Python dependency installation require internet access; once installed, the tutor can run offline.

## Current prototype scope

- Local chat with conversation history for the current browser session.
- Lists locally installed Ollama models and lets you choose one.
- Uses a teaching prompt that encourages clear explanations and paced learning.
- Does not yet ingest documents, save long-term progress, or use LangChain/LangGraph.

The complete project vision and planning options are in [PROJECT_PLAN.md](PROJECT_PLAN.md) and [ORIGINAL_DETAILED_PLAN.txt](ORIGINAL_DETAILED_PLAN.txt).
