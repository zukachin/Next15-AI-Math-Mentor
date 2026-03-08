
---

# Next15 AI Math Mentor: Multimodal RAG

An end-to-end, multi-agent AI system built to solve complex JEE-style mathematics problems. This application utilizes a **Unified Groq Inference** strategy for Image, Audio, and Text processing, ensuring sub-second reasoning and high pedagogical accuracy.

**[Demo video is available in the repo]** 

---

## System Architecture

The mentor utilizes a **Decentralized Multi-Agent Orchestration** pattern. Instead of a single linear prompt, the problem is passed through specialized agents that verify logic and retrieve external context.

### The Agentic Lifecycle

1. **Unified Perception (Groq):** * **Vision:** Llama-4-Scout-17b handles math OCR from screenshots.
* **Audio:** Whisper-Large-V3-Turbo transcribes spoken questions into LaTeX-ready text.


2. **Parser Agent:** Structures the raw input into a JSON format containing variables, constraints, and ambiguity flags.
3. **Intent Router:** Classified the problem (e.g., *Calculus* vs. *Probability*) to load the correct RAG tools.
4. **Hybrid Retrieval:** Combines **RAG** (curated math formulas from ChromaDB) and **Persistent Memory** (previous successful solutions).
5. **Solve & Verify Loop:** The Solver generates a solution, which is immediately audited by the **Verifier Agent** for "hallucinated" steps.
6. **HITL (Human-in-the-Loop):** If the Verifier or OCR confidence is low ($< 0.7$), the system pauses for user confirmation before proceeding.

---

## Tech Stack

* **Inference:** [Groq](https://www.google.com/search?q=https://groq.com/) (Llama-3.3-70b, Llama-4-Scout, Whisper-v3-Turbo)
* **Fallback/OCR Backup:** Google Gemini 2.0 Flash
* **Orchestration:** Custom Python Agentic Framework
* **Vector DB:** ChromaDB (for RAG and Memory)
* **Frontend:** Streamlit
* **Environment:** Python 3.10+

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/math-mentor.git
cd math-mentor

```

### 2. Configure Environment

Create a `.env` file:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run the Mentor

```bash
streamlit run app.py

```

---

## 📂 Project Structure

```text
Backend\math-mentor
├── agents/             # Core Reasoning: Parser, Router, Solver, Verifier, Explainer
├── memory/             # Persistent interaction storage & self-learning logic
├── rag/                # Vector store, document ingestion, and retrieval
├── chroma_db/          # Local vector storage files
├── app.py              # Main Streamlit Multimodal UI
├── config.py           # Unified LLMWrapper for Groq/Gemini routing
└── .env.example        # Template for API keys

```

---

## 📝 Evaluation Summary

* **JEE Domain Coverage:** Algebra, Probability, Calculus, and Linear Algebra.
* **Confidence Scoring:** Implemented in both OCR and Verification stages to ensure HITL reliability.
* **Deployment:** Optimized for Streamlit Cloud.

---