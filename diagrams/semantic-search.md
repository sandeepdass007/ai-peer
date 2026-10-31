# Semantic Search in AI Peer

This diagram shows how AI Peer uses embeddings and cosine similarity to find source paragraphs that are relevant to a learner's question.

The scores are illustrative examples, not scores measured from the app. The current similarity cutoff is `0.4`.

```mermaid
flowchart TD
    Q["Question: How do weights work?"] --> QP["Add search_query prefix"]
    QP --> QE["Ollama converts question into an embedding vector"]

    P1["P1: Training adjusts weights and biases"] --> P1P["Add search_document prefix"]
    P2["P2: Quantum entanglement links particle states"] --> P2P["Add search_document prefix"]
    P1P --> E1["Ollama converts P1 into an embedding vector"]
    P2P --> E2["Ollama converts P2 into an embedding vector"]

    QE --> C["Compare vectors with cosine similarity"]
    E1 --> C
    E2 --> C

    C --> S1["P1 score: 0.63 — above 0.4 cutoff"]
    C --> S2["P2 score: 0.21 — below 0.4 cutoff"]

    S1 --> R["Select P1 and provide it to Gemma with citation [P1]"]
    S2 --> X["Exclude P2"]
    R --> A["Gemma answers using the selected source"]
```

## What the diagram demonstrates

- **Embedding:** Ollama turns text into a vector, a list of numbers representing its meaning.
- **Semantic matching:** A question and passage can use different words and still have similar vectors.
- **Cosine similarity:** AI Peer compares the question vector with each paragraph vector to rank passages by similarity.
- **Cutoff:** AI Peer keeps passages scoring at least `0.4`; it currently returns up to three.
- **Grounded answer:** Selected passages are sent to Gemma as reference material, with their original paragraph IDs for citations.

Nomic uses `search_query:` for questions and `search_document:` for source passages so it can treat each text according to its role in retrieval.
