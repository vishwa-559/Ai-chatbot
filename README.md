# Ai-chatbot
# 🤖 Local AI Chatbot

A chatbot that runs **100% locally** using Ollama (Llama 3.2) with a terminal version and a Streamlit web UI. No API keys needed.

## Features

- Streaming responses
- Conversation memory
- Editable system prompt (web UI)

## Setup

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2
```

Create a `.env` file:

```
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
```

## Run

```bash
python main.py          # terminal chatbot
streamlit run app.py    # web UI
```

## Author

**Vishwa K**
