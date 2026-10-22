# AI Peer Learning Journal

This journal records the learner’s goals, demonstrated understanding, and next steps. Keep observations editable and evidence-based; do not treat one answer as a permanent profile.

## Learner starting point

- Comfortable with Python; experienced Java programmer.
- Learning goal: understand AI and LLM application fundamentals, then apply that knowledge while building AI Peer.
- Preferred direction: guided, paced learning that starts from foundations.
- Preferred learning mode: learner manually types the application code. Teach unfamiliar tools such as Streamlit from the beginning using small code snippets or one function at a time, explain what each part does, then let the learner run it and report back. Review or debug learner-written code rather than implementing features on the learner's behalf. Pause for deeper discussion when it materially helps.

## Session 1 — AI foundations

### Concept: AI, machine learning, deep learning, and generative AI

Introduced the broad relationship between AI, ML, deep learning, and generative AI. The learner explained that ML learns patterns from examples and can classify something as X or Y, while generative AI produces content such as text, images, or video.

### Evidence and current understanding

- Correctly identified classification as an example of machine learning.
- Correctly described generative AI by its ability to create content.
- Next clarification: classification is one ML task; ML also includes regression, clustering, forecasting, and other approaches. Generative AI is a capability/category that often uses ML and deep learning, so it is not separate from ML.

### Next concept

Training vs. inference: how a model’s parameters are adjusted from examples during training, and how a trained model uses those parameters to make a prediction or generate output during inference.

### Concept: training vs. inference

The learner described training as learning and inference as using what was learned. For the example of a model labeling an existing email as spam or not spam, the learner correctly identified the model’s action as inference.

### Evidence and current understanding

- Correctly distinguishes fitting/learning from applying a trained model to a new case.
- Useful nuance to retain: a person labeling emails to create training examples is annotating data; the model trains only when an algorithm uses examples to adjust its parameters. A trained model labeling a new email is inference.

### Next concept

Introduce parameters and the basic training loop: prediction → compare with the expected answer → calculate error → adjust parameters → repeat. Then connect that to how a trained model makes predictions.

## Session 2 — Building the first interface

The learner manually created and ran a minimal Streamlit page in `first_app.py` with a title and welcome text, added a text input that reads a topic, a `Start learning` button, and a warning for an empty topic. The learner confirmed the button and input validation worked. Continue by adding one interactive widget or function at a time, with explanations before each addition.

### Local model and tutor prompt

The learner installed Ollama 0.40.6, downloaded the `gemma4:e4b` model (about 9.5 GB), and confirmed it responds locally without an internet connection. In `first_app.py`, the learner added an `ask_ollama` function that sends a prompt to Ollama's local chat API, then added a system message defining AI Peer as a patient tutor. The learner tested it with a Java lambda question and liked the detailed example. Browser usage statistics were disabled in `.streamlit/config.toml`.

### Conversation history

The learner added a `messages` list in `st.session_state`, changed `ask_ollama` to accept the message history, and appends each user prompt and assistant response. The full transcript is rendered with `st.chat_message` after each Streamlit rerun. The learner confirmed that follow-up prompts are answered with context from earlier messages. The transcript currently displays in chronological order; the learner chose to defer cosmetic changes and keep the focus on functionality.

### Reliability and conversation controls

The learner added `HTTPError` handling for Ollama API errors and `URLError`/`TimeoutError` handling for connection failures in `first_app.py`. The learner tested the unavailable-server case by stopping Ollama in Activity Monitor; AI Peer showed the expected connection message instead of a traceback. The learner also added a **Clear conversation** button that empties `st.session_state.messages`; the transcript is cleared on the resulting rerun. Continue guiding with small explanations and code steps; the learner types the application code.

### First source-grounded tutoring flow

The learner added a `.txt` uploader, reads its UTF-8 contents, and passes the text separately from the visible chat history into `ask_ollama`. The request labels the document as reference material and the system message tells the model to treat it as untrusted source text, use it as evidence, and say when it does not support an answer. A sample neural-network text file was added to the project for practice. The learner confirmed that a question covered by the file was answered from it and that an out-of-scope question was identified as not covered. Current implementation sends the whole small file with each request; relevant-passage retrieval and citations are future work.
