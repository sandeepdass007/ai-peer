# Semantic Search in AI Peer

This diagram shows how AI Peer handles labeled text or PDF sources, chunks them, and uses embeddings and cosine similarity to find relevant passages.

The scores are illustrative examples, not scores measured from the app. The current similarity cutoff is `0.4`.

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

    C --> S1["P4 chunk score: 0.63 — above 0.4 cutoff"]
    C --> S2["Page 2 chunk score: 0.21 — below 0.4 cutoff"]

    S1 --> R["Select best chunk per source; provide it to Gemma with label [P4]"]
    S2 --> X["Exclude Page 2 chunk"]
    R --> A["Gemma answers using the selected source"]
```

## What the diagram demonstrates

- **Embedding:** Ollama turns text into a vector, a list of numbers representing its meaning.
- **Source labels:** Text paragraphs use labels such as `P4`; PDF pages use labels such as `Page 2`. The label stays attached to each passage.
- **PDF extraction:** Selectable page text can be extracted; image-only scanned pages need OCR, which is not implemented yet.
- **Chunking:** Long sources become overlapping word windows. Each chunk keeps its source label as metadata for citations.
- **Semantic matching:** A question and chunk can use different words and still have similar vectors.
- **Cosine similarity:** AI Peer compares the question vector with each chunk vector to rank passages by similarity.
- **Cutoff:** AI Peer keeps chunks scoring at least `0.4`, then returns up to three chunks from distinct source labels.
- **Grounded answer:** Selected passages are sent to Gemma as reference material, with their original paragraph or page labels for citations.

Nomic uses `search_query:` for questions and `search_document:` for source passages so it can treat each text according to its role in retrieval.
