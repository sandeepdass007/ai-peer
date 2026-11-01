# `first_app.py` walkthrough

This document explains why the main parts of `first_app.py` exist and how data moves through the current AI Peer prototype. The app uses Ollama locally for both embeddings and chat, while Streamlit provides the interface and keeps the current conversation in session state.

For a visual version of the semantic retrieval path, see [the semantic-search diagram](../diagrams/semantic-search.md).

## The end-to-end flow

When the learner uploads a text file and asks a question, the app:

1. Reads the UTF-8 text and splits it at blank lines. Each resulting paragraph is the current source unit and keeps a stable number such as `P1`.
2. Embeds the question with the `search_query` prefix.
3. Embeds each source paragraph with the `search_document` prefix. It saves these document embeddings in Streamlit session state so later questions about the same text can reuse them.
4. Compares the question embedding with each paragraph embedding using cosine similarity.
5. Keeps paragraphs scoring at least `0.4`, sorts them from highest to lowest score, and selects up to three.
6. Sends the conversation and selected, labeled passages to the local Gemma chat model.
7. Renders the answer and displays the original source paragraph for each valid citation it contains.

Without an uploaded file, retrieval returns no passages and the tutor can answer as a normal local chat.

## Function guide

| Function | Responsibility | Why it is separate |
|---|---|---|
| `cosine_similarity` | Compares two embedding vectors and returns a similarity score. | Ranking is predictable math; the language model does not need to decide which paragraph is closest. |
| `get_embedding` | Calls Ollama's local embedding API and returns a vector for one text. | Keeps the HTTP request and Nomic task prefixes in one place. |
| `get_paragraph_embeddings` | Builds or reuses embeddings for the uploaded paragraphs. | Embeddings do not change when the question changes, so caching avoids repeating those model calls. |
| `create_chunks` | Splits long paragraphs into word windows with a small overlap, preserving the original paragraph number. | Long source blocks may contain multiple ideas; overlap helps retain context across a split. This helper is currently **not yet connected** to retrieval, which still embeds whole paragraphs. |
| `find_relevant_paragraphs` | Embeds a question, ranks paragraphs, applies the cutoff, and returns the top matches. | Separates retrieval from prompt construction and display. |
| `ask_ollama` | Sends the tutor instructions, conversation history, and retrieved sources to the chat endpoint. | Keeps chat prompting and its HTTP request separate from retrieval. |

## Important concepts in this code

### Embeddings and task prefixes

An embedding is a list of numbers that represents text in a space where related meanings tend to be closer. Nomic uses `search_query:` for questions and `search_document:` for passages so each vector is generated for its role in retrieval. The same embedding model must be used for both sides of a comparison.

The prefixes follow [Nomic's model instructions](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5). Ollama exposes the locally installed model through its [embedding API](https://github.com/ollama/ollama/blob/main/docs/api.md).

### Cosine similarity and the cutoff

Cosine similarity compares vector directions. `find_relevant_paragraphs` uses `SIMILARITY_THRESHOLD` as an initial relevance cutoff and `MAX_RELEVANT_PARAGRAPHS` to limit how much source text is sent to Gemma. These are starting settings; their quality depends on the uploaded material and should be reviewed with representative questions.

### Caching in session state

`get_paragraph_embeddings` uses the tuple of paragraph text as its cache key. If the text is unchanged, it reuses the saved vectors. If the upload changes, it builds a new set. The cache lives in the current Streamlit session; it is not a persistent on-disk embedding database. The terminal messages in this function are temporary diagnostics that show whether the code rebuilt or reused the cache.

### Chunks and citations

The current retrieval unit is one blank-line-separated source paragraph. `create_chunks` is the next step toward handling long paragraphs: each returned item is `(original_paragraph_number, chunk_text)`. Several chunks may share the same paragraph number, which allows retrieved snippets to retain a link to the original source paragraph for citations.

`max_words` controls chunk size, and `overlap_words` repeats trailing words at the beginning of the next chunk. The function checks that the overlap is smaller than the chunk size; otherwise the loop might fail to advance. The helper is present for learning, but the main retrieval path does not use it yet.

## Streamlit interface and state

Streamlit reruns the Python file as the learner interacts with widgets. `st.session_state.messages` preserves the chat transcript across those reruns. The separate embedding cache keys its vectors against the source paragraphs, so questions can change while the source embeddings stay reusable.

The interface has four main areas:

- Topic input and optional `.txt` upload.
- Clear-conversation action.
- Start-learning action, which runs retrieval and chat.
- Transcript rendering, including source text for valid paragraph citations.

## Commenting convention going forward

- Give each reusable function a docstring describing its job and important assumptions.
- Add inline comments for reasoning, constraints, or decisions that are not obvious from the code (for example, why overlap words are repeated).
- Keep comments focused on why the code exists; let clear names explain straightforward operations.
- Update this walkthrough when a new concept changes the data flow or the app's behavior.
