import os
import ollama
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=HOST)

st.set_page_config(page_title="Local AI Chatbot", page_icon="🤖")
st.title("🤖 Local AI Chatbot")
st.caption(f"Running locally with {MODEL}")

with st.sidebar:
    st.header("Settings")
    system_prompt = st.text_area(
        "System prompt", "You are a helpful assistant."
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])


def stream_reply(messages):
    for chunk in client.chat(model=MODEL, messages=messages, stream=True):
        yield chunk["message"]["content"]


if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_messages = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(full_messages))
        except Exception as e:
            st.error(f"Error: {e}. Is Ollama running?")
            st.session_state.messages.pop()
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    