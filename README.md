# AI Peer

AI Peer is a local-first learning companion. Its current Streamlit learning prototype uses a local Ollama model and answers questions from uploaded text or selectable-text PDF material.

## Requirements

- macOS 14 Sonoma or later
- Python 3.11 or later
- Ollama for macOS and a downloaded local model

## Run the current learning prototype

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

4. Start the current learning app:

   ```sh
   python -m streamlit run first_app.py
   ```

Ollama serves the model locally at `http://localhost:11434`. The app uses that local API and does not send prompts to a cloud model. The model download and Python dependency installation require internet access; once installed, the tutor can run offline.

## Current learning app scope

- Local tutoring with conversation history for the current browser session.
- Accepts one `.txt` or selectable-text `.pdf` learning source at a time.
- Uses hybrid retrieval (semantic similarity, keyword matching, and RRF) over overlapping chunks and cites matching paragraphs or PDF pages.
- Shows selected chunks' semantic, keyword, and fused ranks in an expandable retrieval-details panel.
- Caches source chunk embeddings during the current Streamlit session.
- Shows retrieval, embedding, cache, and response-generation status while answering.
- Keeps learner progress across sessions and adaptive learning workflows as future work.

`app.py` is the earlier chat-only prototype. The guided document-grounded app under active development is `first_app.py`.

The complete project vision and planning options are in [PROJECT_PLAN.md](PROJECT_PLAN.md) and [ORIGINAL_DETAILED_PLAN.txt](ORIGINAL_DETAILED_PLAN.txt).

## Learning the prototype

The guided explanation of the learner-authored app is in [docs/first-app-walkthrough.md](docs/first-app-walkthrough.md). The current hybrid-retrieval flow is also shown in [diagrams/semantic-search.md](diagrams/semantic-search.md).
