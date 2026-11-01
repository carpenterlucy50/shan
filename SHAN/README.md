# VoiceOps 2026: ZentroMart Support Agent
## Architecture: Modular Lexical RAG Support Agent

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/balasundaramshanmugaraj/VoiceOps_Project)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![IIT Guwahati x Gnani.ai](https://img.shields.io/badge/Capstone-IIT%20Guwahati%20%C3%97%20Gnani.ai-orange.svg)](https://app.gnani.ai/voice)

- **Public Repository URL:** [https://github.com/balasundaramshanmugaraj/VoiceOps_Project](https://github.com/balasundaramshanmugaraj/VoiceOps_Project)
- **Author:** Balasundaram Shanmugaraj
- **Course:** LLM & Generative AI Course · Consulting & Analytics Club, IIT Guwahati × Gnani.ai
- **Capstone Project:** VoiceOps 2026

---

## Official Run Command (Batch Audio Testing)

Per Page 14 of the Capstone Brief (*"One command that takes a folder of customer audio files, runs your agent on each, and saves its replies (as text and audio) with the document chunks it used"*):

```bash
python run.py --input-dir <path_to_audio_folder> --output-dir <path_to_output_folder>
```

### Example:
```bash
python run.py --input-dir sample_outputs/test_audio --output-dir sample_outputs/batch_audio_results
```

For every input audio file (`<name>.wav`), this command produces:
1. **Synthesized Spoken Reply:** `<name>_reply.wav` (Gnani TTS with voice *Kaveri*, model *timbre-v2.5*)
2. **Text Reply & Retrieved Sources:** `<name>_reply.txt` (Contains customer transcript, agent text answer, and full retrieved section IDs and chunk contents)
3. **Structured JSON Audit:** `batch_processing_summary.json` (Per-file status, transcripts, responses, audio paths, and retrieved evidence)
4. **Tabular Results Spreadsheet:** `batch_results.csv`

---

## 1. Project Overview & Architecture

This repository delivers an end-to-end, production-grade AI customer support agent for **ZentroMart**, a fictional Indian online store selling groceries and electronics. The agent is built following the four capstone milestones:
1. **Prompting an LLM (Step 1 Baseline):** Sets persona and limits, introducing itself as an AI assistant.
2. **Grounding in Documents (Step 2 RAG):** BM25Okapi lexical retrieval over 21 knowledge base documents, enforcing strict policy precedence (`KB-00.1`) and returning section ID provenance (`[RET-2]`, `[REF-2]`, etc.).
3. **Conversational Multi-Turn Handling (Step 3):** Preserves context across turns, enforces identity verification gates (`IDV-1` to `IDV-3`) with phone last 4 digits or pincode, deterministically counts business days skipping warehouse holidays from **20 October 2026**, and escalates high-value damage claims via `create_ticket()`.
4. **Voice Integration with Gnani.ai (Step 4):** Connects Gnani STT and TTS speech models using the official `gnani-vachana` SDK, with speech-normalized text formatting ("writing for the ear").

```
[Customer Audio] ──> [Gnani STT] ──> [Conversation Agent (Brain)] ──> [Gnani TTS] ──> [Spoken Reply .wav]
                                           │               │
                                   [Lexical BM25 RAG] [Mock Tools]
                                    (21 KB Documents)  (Orders & Tickets)
```

---

## 2. Directory Structure

```text
VoiceOps_Project/
├── README.md                      # Comprehensive project documentation & repo links
├── .env.example                   # Environment variable template (no secrets)
├── .gitignore                     # Git rules (excludes .env, venvs, audio, caches)
├── requirements.txt               # Strict project dependencies
├── run.py                         # Unified entry point CLI (batch audio, chat, eval)
├── generate_report.py             # Script to regenerate 3-page technical report PDF
├── report.pdf                     # Capstone 3-page technical evaluation report
├── demo_instructions.md           # 2-minute live demo walkthrough script
├── src/
│   ├── __init__.py
│   ├── knowledge_base.py          # KB parser, precedence ranker & date math
│   ├── retriever.py               # BM25Okapi lexical retrieval engine
│   ├── baseline.py                # Step 1: Prompt-only LLM baseline
│   ├── rag_agent.py               # Step 2: Grounded RAG agent with section ID tracking
│   ├── tools_adapter.py           # Step 3: Identity-gated order lookup & ticket creation
│   ├── conversation_agent.py      # Step 3: Multi-turn dialog manager with state
│   ├── voice_adapter.py           # Step 4: Gnani STT/TTS voice integration & voice_turn()
│   ├── llm_adapter.py             # Multi-provider LLM adapter (OpenAI/Gemini/Anthropic/Local)
│   └── cli.py                     # Interactive terminal CLI
├── tests/
│   ├── test_agent.py              # Automated test suite (all 4 steps)
│   ├── test_person1.py            # Backward-compatible test runner
│   └── test_gnani_live.py         # Live Gnani STT/TTS credential validator
├── evaluation/
│   ├── eval_questions.py          # Step 1 vs Step 2 benchmark runner (52 questions)
│   └── eval_conversations.py      # Step 3 multi-turn benchmark runner (23 conversations)
├── sample_outputs/                # Genuine evaluation benchmarks and batch outputs
│   ├── baseline_results.csv       # Step 1 baseline output records
│   ├── rag_results.csv            # Step 2 grounded RAG output records
│   ├── conversation_results.json  # Step 3 multi-turn turn-by-turn evaluations
│   ├── evaluation_summary.json    # Quantitative metrics comparison
│   └── batch_audio_results/       # Batch run outputs (JSON, CSV, transcripts)
└── submission/
    └── balasundaram_shanmugaraj_voiceops.zip  # Self-contained submission ZIP
```

---

## 3. Installation & Setup

### Prerequisites
- Python 3.10+
- Internet access for Gnani STT/TTS APIs

### Step 1: Clone Repository
```bash
git clone https://github.com/balasundaramshanmugaraj/VoiceOps_Project.git
cd VoiceOps_Project
```

### Step 2: Create Virtual Environment
```bash
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 4. Configuration (`.env`)

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` to configure your credentials:

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=gpt-4o-mini

# Gnani.ai Speech Services (Step 4 Voice)
# Sign up at: https://app.gnani.ai/voice
GNANI_API_KEY=your_actual_gnani_api_key
GNANI_TTS_VOICE=Kaveri
GNANI_TTS_MODEL=timbre-v2.5
GNANI_LANGUAGE_CODE=en-IN
```

> **Note on Security:** As instructed in the Capstone Brief, never commit `.env` or any real API keys to Git. The `.gitignore` file is preconfigured to prevent secret leakage.

---

## 5. Execution Commands

### A. Official Batch Audio Run (Capstone Brief Page 14)
Processes a directory of customer audio files through Gnani STT, the conversational agent, and Gnani TTS:
```bash
python run.py --input-dir <path_to_audio_folder> --output-dir <path_to_output_folder>
```
Example:
```bash
python run.py --input-dir sample_outputs/test_audio --output-dir sample_outputs/batch_audio_results
```

### B. Run Full Practice Evaluation Benchmark
Evaluates the 52 practice questions (Step 1 Baseline vs Step 2 Lexical RAG) and all 23 multi-turn conversations (Step 3):
```bash
python run.py --mode evaluate
```

### C. Interactive CLI Chat (Step 3)
Interact with the agent directly in your terminal:
```bash
python run.py --mode chat
```

### D. Interactive Voice CLI (Step 4)
Speaks answers aloud through Gnani TTS:
```bash
python run.py --mode chat --voice
```

### E. Run Automated Test Suite
Executes all unit and integration tests across data parsing, RAG, business day math, caller verification gates, ticket creation, speech normalization, and voice pipeline:
```bash
python tests/test_agent.py
```

### F. Verify Dataset Integrity
Validates all 9 CSVs, 21 knowledge base documents, and relational keys:
```bash
python Capstone_Project_Dataset_FTTT_2026/validate_dataset.py
```

---

## 6. The Four Capstone Steps Explained

### Step 1: Prompt-Only LLM Baseline (`src/baseline.py`)
- Adopts the ZentroMart support persona.
- Discloses AI identity on the very first turn.
- Answers questions using general knowledge without access to internal documents.
- Establishes the baseline accuracy (88.5% decisions, but only 1.9% fact coverage).

### Step 2: Grounded RAG Agent (`src/rag_agent.py` & `src/retriever.py`)
- Chunks all 21 Markdown files in `kb/`, indexing section headings and section IDs (`[RET-2]`, `[REF-2]`, etc.).
- Enforces policy precedence according to `[KB-00.1]`:
  $$\text{Current Policy} \succ \text{Agent Guide} \succ \text{Help} \succ \text{FAQ} \succ \text{Marketing}$$
- Avoids outdated traps (e.g. `pol_returns_v3_superseded.md` vs `pol_returns_v4.md`, and `FAQ-1` vs `REF-2`).
- Gracefully abstains on unsupported questions ("I don't know" / hand over to a colleague).

### Step 3: Conversational Agent & Tools (`src/conversation_agent.py` & `src/tools_adapter.py`)
- Tracks multi-turn conversation state and session history.
- Resolves contextual follow-ups like *"how long will that take?"* without re-asking order IDs.
- **Caller Verification Gate:** Protects customer data by requiring the last 4 digits of phone or 6-digit delivery pincode (maximum 1 retry) before disclosing order status or items.
- **Deterministic Business Day Math:** Anchored to **20 October 2026**, counting Monday–Saturday and skipping Sundays and listed warehouse holidays (`holidays.csv`).
- **Ticket Escalation:** Creates tickets via `create_ticket()` for damaged goods over ₹10,000, confirming handover only after `created=True`.

### Step 4: Voice with Gnani.ai (`src/voice_adapter.py`)
- Implements the exact 10-line voice turn interface specified on Page 10 of the Capstone Brief:
  ```python
  from gnani.stt import GnaniSTTClient
  from gnani.tts import GnaniTTSClient

  stt = GnaniSTTClient()  # reads GNANI_API_KEY from environment
  tts = GnaniTTSClient()

  def voice_turn(audio_path, agent):
      heard = stt.transcribe(audio_path, language_code="en-IN")["transcript"]
      if not heard.strip():
          reply = "Sorry, I didn't catch that. Could you say it again?"
      else:
          reply = agent.respond(heard)  # Step 3 agent
          tts.synthesize(reply, voice="Kaveri", model="timbre-v2.5",
                         language="en-IN", output_file="reply.wav")
      return heard, reply
  ```
- **Replies for the Ear (Page 11):** Formats long order numbers into spaced pairs (e.g., `8978 2837`), includes the year in dates (`20 October 2026`), and strips markdown syntax before TTS synthesis.
- Gracefully recovers from unclear/silent audio: *"Sorry, I didn't catch that. Could you say it again?"*

---

## 7. Empirical Evaluation Benchmark

The agent was evaluated against all 52 official practice questions and all 23 multi-turn conversations (96 customer turns):

| Metric | Step 1: Baseline | Step 2: Lexical RAG | Step 3: Multi-Turn | Improvement / Benchmark Note |
| :--- | :---: | :---: | :---: | :--- |
| **Decision Accuracy** | 88.5% | 88.5% | **97.9%** | +9.4% multi-turn dialog accuracy |
| **Fact Coverage Rate** | 1.9% | 51.9% | **96.9%** | +95.0% grounded factual truth |
| **Gold Evidence Recall** | 0.0% | 65.4% | **91.2%** | Document section ID provenance verified |
| **Unsupported Abstention** | 0.0% | 60.0% | **100.0%** | Safe decline of unanswerable policy traps |
| **Tool-Call Accuracy** | N/A | N/A | **100.0%** | Zero false-positive order disclosures |
| **Average Turn Latency** | 12 ms | 28 ms | **35 ms** | Real-time voice telephony capable |

---

## 8. Submission ZIP Packaging

Per Page 14 of the Capstone Brief:
```text
balasundaram_shanmugaraj_voiceops.zip
|-- README.md
|-- .env.example
|-- requirements.txt
|-- run.py
|-- src/
|-- report.pdf
|-- demo.mp4
`-- sample_outputs/
```

> **Rules Adherence:**
> - Strictly excludes `.env`, API keys, virtual environments, and dataset copies.
> - Packaged archive is available under `submission/balasundaram_shanmugaraj_voiceops.zip`.

---

## 9. Live Demo Video (2 Minutes)

A complete 120-second demo walkthrough script is detailed in [`demo_instructions.md`](demo_instructions.md):
- **Scene 1 (0:00–0:30):** Grounded policy question (Wallet refund speed, `[REF-2]` outranking `[FAQ-1]`).
- **Scene 2 (0:30–1:00):** Follow-up inquiry and caller identity verification (order `89782837`, last 4 digits `4533`).
- **Scene 3 (1:00–1:30):** High-value damaged TV escalation (`create_ticket()`, human handover).
- **Scene 4 (1:30–2:00):** Gnani STT/TTS voice turn and batch audio command execution.

---

## 10. License & Acknowledgments

- **Course:** LLM & Generative AI Course, Consulting & Analytics Club, IIT Guwahati.
- **Voice Platform:** Gnani.ai Speech Technologies ([app.gnani.ai/voice](https://app.gnani.ai/voice)).
- **Author:** [Balasundaram Shanmugaraj](https://github.com/balasundaramshanmugaraj)
