# LangChain Chatbot

A powerful, privacy-focused AI chatbot built with LangChain and Ollama. Run AI conversations locally on your machine with both CLI and Streamlit web interfaces.

## Features

- **Local & Private**: All conversations run locally on your machine - no data sent to external APIs
- **Dual Interface**: Command-line interface for quick interactions and a beautiful Streamlit web UI
- **Conversation Memory**: Context-aware responses with configurable conversation history
- **Multiple Models**: Support for various Ollama models (Qwen, Llama, Mistral, CodeLlama)
- **Configurable**: Easy customization via environment variables
- **Context Management**: Automatic warnings when approaching context limits

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai) installed and running
- At least one Ollama model pulled (e.g., `ollama pull qwen2.5-coder:3b`)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/macOS
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   cp .env.eample .env
   ```
   Edit `.env` to customize model settings:
   ```env
   MODEL_NAME=qwen2.5-coder:3b
   TEMPERATURE=0.7
   MAX_TURNS=5
   ```

## Usage

### CLI Interface

Run the command-line chatbot:
```bash
python app.py
```

**Commands:**
- Type your message and press Enter to chat
- `clear` - Clear conversation history and start fresh
- `quit` - Exit the application

### Streamlit Web Interface

Launch the beautiful web interface:
```bash
streamlit run streamlit_app.py
```

The web interface provides:
- Real-time chat with typing indicators
- Model selection dropdown
- Temperature and max turns sliders
- Conversation statistics
- Dark theme with gradient styling

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | Ollama model to use | `qwen2.5-coder:3b` |
| `TEMPERATURE` | Response creativity (0.0-1.0) | `0.7` |
| `MAX_TURNS` | Maximum conversation turns before context reset | `5` |

## Available Models

The application supports any Ollama-compatible model. Popular options:

| Model | Size | Best For |
|-------|------|----------|
| `qwen2.5-coder:3b` | 3B | Code assistance, general chat |
| `llama3.2:3b` | 3B | General purpose conversations |
| `mistral:7b` | 7B | Complex reasoning, detailed responses |
| `codellama:7b` | 7B | Programming and code generation |

Pull a model with:
```bash
ollama pull <model-name>
```

## Project Structure

```
langchain-chatbot/
├── app.py              # CLI chatbot application
├── streamlit_app.py    # Streamlit web interface
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── .env.eample         # Environment variables template
└── README.md           # This file
```

## Technology Stack

- **[LangChain](https://langchain.com)** - Framework for LLM applications
- **[Ollama](https://ollama.ai)** - Local LLM inference
- **[Streamlit](https://streamlit.io)** - Web interface framework

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is open source and available under the [MIT License](LICENSE).