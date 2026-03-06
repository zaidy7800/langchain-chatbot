# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run CLI chatbot
python app.py

# Run Streamlit web interface
streamlit run streamlit_app.py
```

## Architecture

This is a LangChain-based chatbot that runs locally using Ollama for LLM inference.

**Core Components:**
- `app.py` - CLI interface with interactive chat loop
- `streamlit_app.py` - Streamlit web UI with session state management

**LLM Pipeline:**
Both interfaces share the same LangChain architecture:
- `ChatPromptTemplate` with system message + conversation history + user input
- `ChatOllama` for local model inference
- `StrOutputParser` for response handling

**Conversation Management:**
- Chat history stored as list of `HumanMessage` and `AIMessage` objects
- `MAX_TURNS` limits conversation length to prevent context overflow
- Users can clear history via `clear` command (CLI) or "Clear Chat" button (web)

**Configuration:**
Environment variables in `.env` (copy from `.env.eample`):
- `MODEL_NAME` - Ollama model (default: `qwen2.5-coder:3b`)
- `TEMPERATURE` - Response randomness 0.0-1.0 (default: `0.7`)
- `MAX_TURNS` - Conversation turn limit (default: `5`)

**Prerequisites:**
- Ollama must be running locally (`ollama serve`)
- At least one model pulled (`ollama pull <model>`)