# Hybrid Retrieval in AI Peer

This diagram shows how AI Peer combines semantic similarity with exact keyword matching, then uses Reciprocal Rank Fusion (RRF) to rank relevant passages from labeled text or PDF sources.

The scores and ranks are illustrative examples, not values measured from the app. The current semantic similarity cutoff is `0.4`; RRF uses a rank constant of `60`.

```mermaid
flowchart TD
    Q["Question: How do weights work?"] --> QP["Add search_query prefix"]
    QP --> QE["Ollama converts question into an embedding vector"]

    P1["Text paragraph about training weights"] --> P1L["Label source P4"]
    P2["PDF page about quantum entanglement"] --> P2L["Extract selectable text; retain Page 2"]
    P1L --> CH["Split into overlapping word chunks; retain source label P4"]
    P2L --> CH2["Split into word chunks; retain source label Page 2"]
    CH --> P1P["Add search_document prefix to each chunk"]
    CH2 --> P2P["Add search_document prefix to each chunk"]
    P1P --> E1["Ollama converts chunk text into an embedding vector"]
    P2P --> E2["Ollama converts chunk text into an embedding vector"]
    E1 --> CACHE["Cache chunk vectors for reuse while source text stays the same"]
    E2 --> CACHE

    QE --> C["Compare vectors with cosine similarity"]
    CACHE --> C

    C --> SL["Semantic ranking; keep scores at least 0.4"]
    Q --> KW["Tokenize question and chunk; ignore stop words"]
    CH --> KW
    KW --> KL["Keyword ranking by fraction of question terms matched"]

    SL --> F["RRF adds 1 / (60 + rank) from each ranking"]
    KL --> F
    F --> R["Sort by fused score; select up to three distinct source labels"]
    R --> A["Send selected labeled sources to Gemma"]
    R --> D["Show selected chunks and their semantic, keyword, and fused ranks in an expander"]
    A --> OUT["Answer cites the source label, such as [P4] or [Page 2]"]
```

## What the diagram demonstrates

- **Embedding:** Ollama turns text into a vector, a list of numbers representing its meaning.
- **Source labels:** Text paragraphs use labels such as `P4`; PDF pages use labels such as `Page 2`. The label stays attached to each passage.
- **PDF extraction:** Selectable page text can be extracted; image-only scanned pages need OCR, which is not implemented yet.
- **Chunking:** Long sources become overlapping word windows. Each chunk keeps its source label as metadata for citations.
- **Semantic matching:** A question and chunk can use different words and still have similar vectors.
- **Keyword matching:** AI Peer scores the fraction of useful question terms that appear in each chunk. This can help with exact names and terminology but does not itself match synonyms.
- **Reciprocal Rank Fusion:** The semantic and keyword lists have different score scales. RRF combines their rank positions by adding `1 / (60 + rank)` for each list containing a chunk, avoiding a hand-tuned weighted sum of raw scores.
- **Selection:** The semantic list applies the `0.4` cutoff; the keyword list keeps chunks with at least one matching useful term. AI Peer fuses the lists, then returns up to three chunks from distinct source labels.
- **Retrieval diagnostics:** The expandable panel shows selected chunks' semantic rank and score, keyword rank and score, and final fused rank and score. It helps explain the evidence selected for the answer; it does not display every candidate chunk.
- **Grounded answer:** Selected passages are sent to Gemma as reference material, with their original paragraph or page labels for citations.

RRF preserves the order of each input ranking but ignores the size of score gaps. The rank constant `60` is a fixed baseline here, not a value tuned against a benchmark for this project.

Nomic uses `search_query:` for questions and `search_document:` for source passages so it can treat each text according to its role in retrieval.
