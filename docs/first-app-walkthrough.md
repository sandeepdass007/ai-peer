# `first_app.py` walkthrough

This document explains why the main parts of `first_app.py` exist and how data moves through the current AI Peer prototype. The app uses Ollama locally for both embeddings and chat, while Streamlit provides the interface and keeps the current conversation in session state.

For a visual version of the semantic retrieval path, see [the semantic-search diagram](../diagrams/semantic-search.md).

## The end-to-end flow

When the learner uploads a text or PDF file and asks a question, the app:

1. Reads a `.txt` file as UTF-8 and splits it at blank lines, labeling paragraphs `P1`, `P2`, etc. For a `.pdf`, `extract_pdf_pages` extracts selectable text page by page and retains each one-based page number.
2. Converts either kind of input into labeled source records such as `("P1", text)` or `("Page 1", text)`. Scanned image-only PDF pages do not provide selectable text and are skipped; OCR is not implemented yet.
3. Splits each labeled source into word-based chunks. The default chunk size is 150 words with 25 words of overlap; each chunk retains its source label.
4. Embeds the question with the `search_query` prefix.
5. Embeds each chunk's text with the `search_document` prefix. It caches these vectors in Streamlit session state so later questions about the same chunks can reuse them.
6. Compares the question embedding with each chunk embedding using cosine similarity.
7. Keeps chunks scoring at least `0.4`, sorts them from highest to lowest score, then selects up to three chunks from distinct source labels.
8. Sends the conversation and selected, labeled chunk text to the local Gemma chat model. The system prompt lists the exact labels available for this answer, such as `[P4]` or `[Page 3]`, to help the model cite the right source type.
9. Renders the answer and displays the original source text for each citation that matches the current upload.

Without an uploaded file, retrieval returns no passages and the tutor can answer as a normal local chat.

## Function guide

| Function | Responsibility | Why it is separate |
|---|---|---|
| `cosine_similarity` | Compares two embedding vectors and returns a similarity score. | Ranking is predictable math; the language model does not need to decide which paragraph is closest. |
| `get_embedding` | Calls Ollama's local embedding API and returns a vector for one text. | Keeps the HTTP request and Nomic task prefixes in one place. |
| `extract_pdf_pages` | Extracts selectable text from each PDF page and returns `(page number, text)` pairs. | Keeping page numbers with extracted text supports page citations. |
| `create_chunks` | Splits labeled sources into overlapping word windows and preserves each source label. | Long source blocks may contain multiple ideas; overlap helps retain context across a split. |
| `get_chunk_embeddings` | Builds or reuses one embedding per chunk and reports chunk counts through the status container. | Source chunks do not change when the question changes, so caching avoids repeating those model calls; the status label shows whether vectors are being built or reused. |
| `find_relevant_paragraphs` | Embeds a question, ranks chunks, applies the cutoff, and returns the strongest matches from distinct source labels. It passes the optional status container to embedding work. | Separates retrieval from prompt construction and display while avoiding repeated citations from one long paragraph or page. |
| `ask_ollama` | Sends the tutor instructions, conversation history, and retrieved sources to the chat endpoint. | Keeps chat prompting and its HTTP request separate from retrieval. |

## Important concepts in this code

### Embeddings and task prefixes

An embedding is a list of numbers that represents text in a space where related meanings tend to be closer. Nomic uses `search_query:` for questions and `search_document:` for passages so each vector is generated for its role in retrieval. The same embedding model must be used for both sides of a comparison.

The prefixes follow [Nomic's model instructions](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5). Ollama exposes the locally installed model through its [embedding API](https://github.com/ollama/ollama/blob/main/docs/api.md).

### Cosine similarity and the cutoff

Cosine similarity compares vector directions. `find_relevant_paragraphs` uses `SIMILARITY_THRESHOLD` as an initial relevance cutoff and `MAX_RELEVANT_PARAGRAPHS` to limit how much source text is sent to Gemma. These are starting settings; their quality depends on the uploaded material and should be reviewed with representative questions.

### Caching in session state

`get_chunk_embeddings` uses the tuple of `(source label, chunk text)` pairs as its cache key. If the chunks are unchanged, it reuses the saved vectors. If the upload or chunk boundaries change, it builds a new set. The cache lives in the current Streamlit session; it is not a persistent on-disk embedding database. When a status container is passed in, the app reports each embedding count during a build and identifies a cache hit. The terminal messages are temporary diagnostics that show the same build-versus-reuse distinction.

### Chunks and citations

The current retrieval unit is a chunk; its original source label is retained as metadata. Each item returned by `create_chunks` is `(source_label, chunk_text)`. A text paragraph uses a label such as `P4`; a PDF page uses `Page 3`. Several chunks may share a label, which lets retrieved snippets link back to the correct original passage.

`max_words` controls chunk size, and `overlap_words` repeats trailing words at the beginning of the next chunk. The function checks that the overlap is smaller than the chunk size; otherwise the loop might fail to advance. Retrieval keeps only the best-scoring chunk for each source label, then takes up to three distinct sources.

## Streamlit interface and state

Streamlit reruns the Python file as the learner interacts with widgets. `st.session_state.messages` preserves the chat transcript across those reruns. The embedding cache keys vectors against the source chunks, so questions can change while the source embeddings stay reusable.

The **Start Learning** flow uses `st.status` to show the current task stage. It reports retrieval, embedding progress when chunks are rebuilt, cache reuse when they are unchanged, and answer generation. It uses a count for embedding work rather than a percentage because the number of chunks is known while each chunk is processed.

The interface has four main areas:

- Topic input and optional `.txt` or `.pdf` upload.
- Clear-conversation action.
- Start-learning action, which runs retrieval and chat.
- Status container, which reports retrieval, embedding, cache, and generation stages.
- Transcript rendering, including source text for valid paragraph or page citations.

## Commenting convention going forward

- Give each reusable function a docstring describing its job and important assumptions.
- Add inline comments for reasoning, constraints, or decisions that are not obvious from the code (for example, why overlap words are repeated).
- Keep comments focused on why the code exists; let clear names explain straightforward operations.
- Update this walkthrough when a new concept changes the data flow or the app's behavior.
