# Agentic SWE Team Simulator 

A fully autonomous, multi-agent software engineering team built with **LangGraph**, **LangChain v1.0**, and the **Groq API**. 

This system simulates a four-person AI agency that takes a vague user prompt, translates it into technical specs, writes the source code, physically executes tests on your local machine, and generates documentation—looping autonomously until the code passes Quality Assurance.

## How It Works

The system relies on a shared memory dictionary (`TeamState`) and routes between four specialized agents:

1. **Product Manager:** Translates user requests into strict technical requirements (`specs.txt`).
2. **Software Engineer:** Reads the specs and writes raw Python code (`app.py`), outputting standard Markdown to prevent JSON string-escaping errors.
3. **QA Engineer:** Writes a test script (`test_app.py`), executes it locally, and uses an LCEL chain to output a strict Pass/Fail decision for deterministic routing.
4. **Documentation Writer:** Reads the final validated codebase and generates a clean `README.md`.

**The Flow:** `START` ➔ `PM` ➔ `SWE` ➔ `QA` ➔ **[Router]** ➔ (Fail: Back to `SWE` | Pass: `Docs`) ➔ `END`

## Key Features

* **Local File System Grounding:** Agents read, write, and execute real files in an isolated `./workspace/` directory.
* **Resilient Code Generation:** Bypasses common LLM tool-hallucination errors by using Python regex to extract code from standard Markdown blocks.
* **LCEL Structured Output:** Guarantees type-safe graph routing by piping QA text evaluations into strict Pydantic schemas.
* **Infinite Loop Protection:** Hard-capped iterations prevent the SWE and QA agents from getting stuck in endless debugging loops.

## Usage

Run the main orchestrator script:

```bash
python main.py
