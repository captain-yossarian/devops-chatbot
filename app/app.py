import os

import streamlit as st
from openai import OpenAI

# Injected by Docker Compose from the `llm` model provider service
# (<SERVICE_NAME>_URL and <SERVICE_NAME>_MODEL).
LLM_URL = os.getenv("LLM_URL", "http://localhost:12434/engines/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "ai/smollm2")

client = OpenAI(base_url=LLM_URL, api_key="not-needed")

st.set_page_config(page_title="DevOps Chatbot", page_icon="🤖")
st.title("🤖 DevOps Chatbot")
st.caption(f"Model: `{LLM_MODEL}` via Docker Model Runner")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=LLM_MODEL,
                messages=st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
                if chunk.choices
            )
        except Exception as e:
            reply = f"⚠️ Error talking to the LLM at `{LLM_URL}`: {e}"
            st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
