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

### Paragraph citations and source display

The source text is split at blank lines and labeled with paragraph IDs such as `[P1]`. AI Peer is instructed to cite only IDs in the supplied material and not follow instructions embedded in that material. The transcript renderer finds IDs in assistant answers, maps them back to the uploaded paragraphs, and shows each valid cited passage once under the answer. The learner confirmed the answer cited the expected paragraph and noticed that repeated citations caused duplicate passages; duplicates are now removed while preserving order. Next, begin selecting only relevant paragraphs for a question so larger files do not all need to be sent to the model.

### Semantic retrieval, embeddings, and caching

The learner added local semantic retrieval using Ollama's `nomic-embed-text` model. The app embeds questions with Nomic's `search_query` prefix and source paragraphs with `search_document`, compares vectors with cosine similarity, applies an initial `0.4` cutoff, and selects up to three passages. The learner reported that “How weights work?” found relevant material while an unrelated quantum-entanglement question did not. The learner also added a session-state cache keyed by source paragraph text so document embeddings can be reused across questions in the same session.

The learner asked that new concepts, libraries, and technologies be explained before implementation, and requested comments and documentation explaining why the code exists. Going forward, use function-sized guided steps, include purposeful docstrings/comments with code suggestions, review their edits directly, and update the walkthrough when the data flow or concepts change.

### Chunking

The learner added a `create_chunks` helper that splits long paragraphs into overlapping word windows while retaining each original paragraph number for citations, then added a cached `get_chunk_embeddings` helper. Semantic retrieval now embeds and ranks chunks, selects the best chunk from up to three distinct source paragraphs, and returns the original paragraph IDs with the selected text. The user manually typed and corrected the code; its Python syntax was checked. Keep the walkthrough and diagram current as the retrieval flow changes. A useful next check is to run the app on answerable and unrelated questions with source material that includes at least one paragraph longer than the 150-word chunk limit.

### PDF text extraction and source labels

The learner added `pypdf` and an `extract_pdf_pages` helper that returns selectable PDF text paired with one-based page numbers. Retrieval source records now carry labels (`P1` for text paragraphs and `Page 1` for PDF pages) through chunking, embedding cache keys, prompt construction, and answer citation display. The learner manually typed the code in guided steps. Image-only scanned PDF pages are not handled yet and will require OCR. Next, manually try a text file and a text-based PDF and observe whether answers cite the appropriate source labels and show their original text.

### Processing status and citation labels

The learner replaced the generic spinner around question handling with a Streamlit status container that reports retrieval, embedding, cache reuse, and answer-generation stages. During a fresh source embedding pass it displays the completed chunk count; when the source chunks are unchanged it reports that cached embeddings are being reused. The learner tested the build and cache status on repeated questions. The chat prompt now receives the exact citation labels retrieved for the current question, which helps the model preserve `P#` labels for text files and `Page #` labels for PDFs. The learner confirmed PDF citations and source captions display correctly. The README launch command now points to `first_app.py`, the document-grounded app, rather than the earlier chat-only `app.py` prototype.

### Hybrid retrieval with keyword matching and RRF

The learner added a keyword score that measures what fraction of the question's non-stop-word terms occur in a source chunk. This complements semantic similarity: embeddings can retrieve paraphrases and related meanings, while exact-term matching can help with distinctive words, names, and terminology. The learner then added Reciprocal Rank Fusion (RRF) to combine the two sorted result lists. RRF adds `1 / (k + rank)` for each list in which a chunk appears, using `k = 60`; it combines positions rather than comparing the raw cosine and keyword scores, whose scales differ. The semantic list still applies the existing `0.4` cutoff, and chunks with no keyword overlap are omitted from the keyword list.

The choice of RRF is a simple baseline for combining differently scaled rankings without inventing and tuning a weighted score such as `0.7 * semantic + 0.3 * keyword`. Its tradeoff is that rank positions matter, while the size of a score gap is ignored. The learner tried a question using different wording and synonyms and confirmed that AI Peer still retrieved PDF content and showed page citations. Repeated citations to the same page in the generated answer are expected when several claims use that page; they do not by themselves reveal which retrieval signals contributed. Further evaluation can compare exact-term and paraphrased questions and inspect retrieval results if a diagnostic view is added later.
