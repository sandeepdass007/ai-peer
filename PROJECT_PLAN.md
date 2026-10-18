# AI Peer — Project Plan

## Purpose

AI Peer is a local AI learning companion that teaches a topic from the learner’s current level toward mastery. It should adapt to the learner’s pace, explain one concept at a time, identify gaps, provide practice, and remember progress between sessions. It should use the learner’s materials—such as YouTube transcripts, books, PDFs, and presentations—as grounded teaching sources.

This document is a compact overview and navigation aid. The complete original ChatGPT planning response, preserved verbatim with all detailed suggestions and alternatives, is in [ORIGINAL_DETAILED_PLAN.txt](ORIGINAL_DETAILED_PLAN.txt). Treat that full document as the source of the broad option set; this overview does not replace or narrow it. We can add decisions and implementation findings here while keeping the original intact.

## Product vision

For a given course or topic, AI Peer should be able to:

1. Assess the learner’s goals, current understanding, and prerequisites.
2. Build a manageable, prerequisite-aware learning path.
3. Find relevant passages in supplied material and cite them.
4. Teach in small steps, adapting explanations when the learner struggles.
5. Create useful diagrams, examples, exercises, quizzes, and feedback.
6. Record demonstrated understanding and resume learning later.
7. Export useful learning artifacts such as notes, flashcards, PDFs, and presentations.

The central principle is: **adapt the system to the learner, rather than forcing the learner to adapt to the system.** AI Peer should be a learning system powered by AI, not just a chatbot connected to documents.

## Architectural principles

- Start as a **modular monolith**. Keep clear module boundaries, but avoid microservices until a concrete need emerges.
- Build one complete learning journey before adding broad platform capabilities.
- Use deterministic functions for predictable tasks such as parsing documents, saving results, and exporting files. Use LLM workflows where reasoning or language generation helps.
- Keep learner progress as explicit, queryable records. Workflow checkpoints are useful for resuming an interrupted interaction, but do not replace the learner database.
- Make mastery evidence-based. Reading an explanation alone does not establish mastery.
- Keep learner profiles editable; model-generated estimates should be treated as tentative evidence, not unquestionable facts.
- Treat uploaded material as untrusted source content. It must not override application instructions or authorize tools.
- Add specialized agents only when each has a clear responsibility and measurable value. Begin with one local model and structured prompts/tools.
- Validate current library versions, hardware fit, and integration compatibility when implementation choices are made.

## Logical architecture

1. **Interface:** chat/lesson view, course and topic selection, uploads, quizzes, progress, diagrams, and exports.
2. **Application backend:** manages courses, lessons, learner state, requests, and tool routing.
3. **Teaching workflows:** stateful tutoring, assessment, ingestion, and revision flows. LangGraph is the proposed workflow orchestrator; LangChain can provide model and document integrations where useful.
4. **Learning and knowledge layer:** original files, extracted text, citations, retrieval index, concept relationships, course structure, and learner progress.
5. **Local runtime:** local language and embedding models, storage, and processing. Initial preference is Ollama, subject to hardware and model evaluation.

Initial teaching loop:

`Understand request → check learner state and prerequisites → retrieve source material → teach one concept → ask a targeted question → evaluate answer → update progress → advance or reteach`

## Knowledge engine

Use a staged retrieval pipeline:

`Source files → extract → clean → structure-aware chunking → embeddings/index → retrieve → rerank (if useful) → grounded answer with citations`

Initial source formats: PDF, PPTX, and plain-text transcripts. Preserve metadata such as document title, chapter/section, page or slide range, and chunk identity so answers can cite sources and return to their location. Scanned PDFs may require OCR or layout-aware parsing later.

The proposed retrieval approach is hybrid:

- Vector retrieval for semantic matches.
- Keyword retrieval for exact terms, acronyms, and identifiers.
- Metadata filters for course, document, chapter, or lesson.
- Optional reranking after the initial retrieval works reliably.

Combine source retrieval with learner-aware concept prerequisites. Begin with a simple in-process graph representation; consider a dedicated graph database only when relationship queries and persistence justify it.

## Learner model and memory

Track at least course goals, current lesson, learner-stated level, preferred pace/style, completed exercises, areas to revisit, and mastery evidence. Keep four concerns distinct:

- Recent conversation context for the current session.
- Episodic learning events, such as a misconception or successful exercise.
- Semantic knowledge about concepts and their relationships.
- Structured learner progress and revision state.

The learner should be able to inspect and correct profile and progress data.

## Agent and capability roadmap

Potential capabilities, introduced incrementally:

- Tutor: explain and answer questions.
- Curriculum: create and adjust prerequisite-aware learning paths.
- Research: retrieve and synthesize source-grounded material.
- Assessment: generate exercises and evaluate responses against a rubric.
- Diagram: produce structured visual explanations.
- Coding: explain code and create programming exercises.
- Content: create reusable notes and exports.
- Review: identify gaps and plan revision/flashcards.

These do not all need to be autonomous LLM agents. Several should be ordinary tools or constrained workflows. Diagram output should favor accurate structured formats such as Mermaid or Graphviz before image generation.

## Proposed starting stack (to validate before adoption)

| Area | Initial candidate | Notes |
|---|---|---|
| Language | Python | Main application and AI ecosystem |
| Local model runtime | Ollama | Start with one suitable local instruct model |
| Model/document integrations | LangChain | Use selectively for integrations and reusable components |
| Stateful workflows | LangGraph | Teaching flow, conditional routing, and resumability |
| Backend | FastAPI | API boundary if/when needed |
| First interface | Streamlit | Fast way to validate the learner experience |
| Relational data | SQLite | Courses, learner progress, and application data |
| Vector retrieval | Chroma or Qdrant | Choose after a small proof of fit |
| Concept graph | Python graph structures initially | Defer dedicated graph database |
| PDF extraction | PyMuPDF | Validate against representative documents |
| PowerPoint | python-pptx | Ingestion and later export |
| Diagrams | Mermaid / Graphviz | Structured and reproducible visuals |
| PDF export | ReportLab | Add with content studio phase |
| Transcription | Whisper | Add when audio/video ingestion is in scope |
| Evaluation | pytest plus custom evaluation cases | Build as behavior is introduced |

The source plan also mentions Neo4j as a possible later graph store and PostgreSQL/pgvector if concurrency or deployment needs outgrow the initial local design. These are options, not commitments.

## Development roadmap

### Phase 1 — Local tutor

Set up Python, Ollama, one local model, a simple Streamlit interface, a beginner-friendly teaching prompt, and conversation history. **Outcome:** useful local tutoring without cloud LLM calls.

### Phase 2 — Document ingestion and RAG

Add PDF/PPTX/transcript ingestion, extraction, cleaning, chunking, embeddings, vector storage, retrieval, and source citations. **Outcome:** answers grounded in uploaded material with inspectable supporting passages.

### Phase 3 — Learner profile and progress

Add courses, topics, goals, lesson state, quiz results, mastery records, and session resumption. **Outcome:** learning progress survives app restarts.

### Phase 4 — Adaptive teaching workflow

Add learning objectives, prerequisite checks, question generation, answer evaluation, targeted feedback, conditional routing, reteaching, and lesson progression. Introduce LangGraph here if it has not already proven useful. **Outcome:** incomplete understanding triggers targeted practice or explanation.

### Phase 5 — Knowledge graph

Represent concepts and prerequisite relationships, support traversal and concept maps, then use graph information in lesson planning and retrieval. Start in-process; add a graph database only when warranted. **Outcome:** identify and address missing prerequisites.

### Phase 6 — Content studio

Generate structured notes, flashcards, quiz sheets, diagrams, PDFs, and presentations. **Outcome:** lessons can be reused and exported in useful formats.

### Phase 7 — Specialized and multimodal capabilities

Selectively add coding exercises, transcription, speech, image understanding, and specialized workflows. **Outcome:** the tutor chooses suitable capabilities for a learning task.

### Phase 8 — Product polish and packaging

Improve error handling, migrations, logging, backup/restore, model management, local security, settings, and optional desktop packaging. **Outcome:** a dependable app that can be launched, updated, and recovered without manual internal maintenance.

## First end-to-end learning journey

The first learning journey will be **AI and LLM application fundamentals**, chosen by the learner. Use it to build both the learner’s understanding and, later, to validate AI Peer itself. A possible progression is: AI vs. machine learning vs. deep learning vs. generative AI; data, models, training, and inference; neural network and transformer foundations; tokens and context; prompting and model limitations; embeddings and retrieval; RAG; tool use and workflows; evaluation and safety; local model application design. Adjust pace and depth based on the learner’s starting point. The original plan’s Introduction to Neural Networks example remains a useful alternative course and is preserved in the full detailed plan.

When the app reaches its document-grounded milestone, use supplied learning materials and explicit objectives to validate the complete path: assess → plan → retrieve → teach → visualize → practice → evaluate → adapt → save → export. This should validate the core product before broadening formats or agents.

## Risks to design for

- Model hallucinations: ground lessons in retrieved evidence and evaluate factual quality.
- Retrieval misses: combine semantic, keyword, and metadata search; consider reranking after a baseline.
- Advancing too quickly or repeating: use explicit mastery evidence and track prior teaching attempts.
- Incorrect concept relations: preserve provenance and validate extracted relationships.
- Prompt injection in documents: treat source text as data, separate it from instructions, and restrict tools.
- Unsafe code execution: isolate exercise execution and restrict permissions if introduced.
- Model updates changing behavior: retain repeatable evaluation cases.
- Data loss or corruption: use transactions, backups, and migrations as the product matures.
- Scope growth: complete one learning journey before expanding subsystems.

## Deliberately deferred

Do not begin with a large autonomous multi-agent system, a dedicated graph database, every document format, local image generation, fine-tuning, a complex frontend, or agents with unrestricted computer access. Add each only when the learning experience demonstrates a real need.

## Decisions to make before implementation

1. **Hardware:** iMac with Apple M4 and 24 GB memory. Check available disk space and validate model performance during setup.
2. **Programming experience:** comfortable with Python and experienced with Java. Guidance can assume programming fundamentals while explaining AI-specific concepts and tradeoffs.
3. **Meaning of standalone:** local-first, capable of working both offline and with internet access. Optional internet can support permitted source retrieval or updates; the first version should not depend on cloud inference.
4. **Future product direction:** licensing and offering the app offline or online are possibilities to keep in mind, not requirements for the first version. Keep boundaries clean enough to allow future options and review model/dependency licenses before any distribution.

## Current starting direction

Begin with a local tutor and one local model, then add source-grounded learning and progress tracking. Do not commit to an online service, cloud storage, or commercial packaging in the first milestone. Select concrete models and versions when we set up the environment, based on current compatibility and measured performance on the M4 with 24 GB memory.

### Phase 1 progress

- Created a first Streamlit tutor prototype in `app.py` that calls Ollama’s local chat API and lists installed local models.
- Added setup instructions and project-local dependency metadata.
- Installed Streamlit into `.venv` and started the app at `http://127.0.0.1:8501`.
- Installed Ollama 0.40.6 and downloaded `gemma4:e4b` (about 9.5 GB); the learner confirmed the model responds locally.
- The learner's manually written `first_app.py` now calls Ollama and includes a tutor-focused system message. `app.py` is a separate reference prototype with session-based conversation history.
- Added `.streamlit/config.toml` with browser usage statistics disabled.

## Working agreement for this project

Use this plan as the baseline and maintain decisions and changes here (or in linked project docs) so project knowledge persists across separate chats. The learner writes the application code; guide with small implementation steps, explain concepts as they arise, and review or debug learner-written code. Pause for deeper discussion when a concept materially affects a design decision. Before choosing versions or implementing fast-changing libraries, verify current compatibility and fit.
