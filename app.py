"""AI Peer: first local tutor prototype."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st


OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:e4b"
SYSTEM_PROMPT = """You are AI Peer, a patient, accurate learning companion.
Teach at the learner's pace. Explain unfamiliar ideas in clear steps, use
concrete examples, and connect new ideas to what the learner already knows.
Answer the learner's actual question before adding extra material. Check
understanding with one focused question when useful. If uncertain, say so.
Do not pretend to have read sources that were not provided."""


def get_installed_models() -> list[str]:
    """Return model names from the local Ollama server, or an empty list."""
    request = Request(f"{OLLAMA_BASE_URL}/api/tags", method="GET")
    with urlopen(request, timeout=2) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [model["name"] for model in payload.get("models", []) if model.get("name")]


def ask_ollama(model: str, messages: list[dict[str, str]]) -> str:
    """Send the current conversation to Ollama's local chat API."""
    payload = json.dumps(
        {
            "model": model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
            "stream": False,
        }
    ).encode("utf-8")
    request = Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError("Could not reach Ollama at http://localhost:11434.") from error

    answer = result.get("message", {}).get("content", "").strip()
    if not answer:
        raise RuntimeError("Ollama returned an empty response.")
    return answer


st.set_page_config(page_title="AI Peer", page_icon="🧭", layout="centered")
st.title("🧭 AI Peer")
st.caption("A local tutor that learns at your pace. This prototype sends prompts only to Ollama running on this computer.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Local model")
    try:
        installed_models = get_installed_models()
        if installed_models:
            default_index = (
                installed_models.index(DEFAULT_MODEL)
                if DEFAULT_MODEL in installed_models
                else 0
            )
            selected_model = st.selectbox("Choose an installed model", installed_models, index=default_index)
            st.success("Ollama is connected")
        else:
            selected_model = st.text_input("Model name", value=DEFAULT_MODEL)
            st.info("Ollama is running, but no models are installed yet.")
    except (HTTPError, URLError, TimeoutError, OSError):
        installed_models = []
        selected_model = st.text_input("Model name", value=DEFAULT_MODEL)
        st.warning("Ollama is not reachable. Start Ollama to enable tutoring.")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    with st.expander("First-time setup"):
        st.markdown(
            """1. Install [Ollama for macOS](https://ollama.com/download/mac).
2. In Terminal, run `ollama pull gemma4:e4b` to download a starter model.
3. Keep Ollama running, then refresh this page."""
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to learn?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking locally…"):
            try:
                answer = ask_ollama(selected_model.strip(), st.session_state.messages)
            except (RuntimeError, HTTPError, URLError, TimeoutError, OSError) as error:
                answer = (
                    f"I couldn't get a response from the local model. {error}\n\n"
                    f"Check that Ollama is running and that `{selected_model}` is installed."
                )
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
