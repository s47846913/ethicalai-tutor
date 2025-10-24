# app.py
import os
import streamlit as st
from prompts import SYSTEM_PROMPT, SCENARIOS, REFLECTION_PROMPT
from utils import get_client, get_model, build_messages
from safety import basic_screen

st.set_page_config(page_title="EthicalAI Tutor", page_icon="🤖", layout="centered")

st.title("🤖 EthicalAI Tutor")
st.caption("Level 6 project — Generative AI educational chatbot for HCAI")

with st.sidebar:
    st.subheader("About")
    st.write(
        "This chatbot demonstrates Human-Centred AI principles: clarity, "
        "explanations, and safe responses. Try asking about fairness, bias, "
        "privacy, transparency, or accountability."
    )
    st.markdown("**Scenario ideas**")
    for s in SCENARIOS:
        st.markdown(f"- {s}")
    st.divider()
    st.markdown("**Quick reflection template**")
    st.code(REFLECTION_PROMPT, language="markdown")
    st.divider()
    st.markdown("**Model**")
    st.write(os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    st.markdown("Set in `.env` → `OPENAI_MODEL`.")

if "history" not in st.session_state:
    st.session_state.history = []

# Chat window
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_text = st.chat_input("Ask about HCAI — e.g., fairness in model design")
if user_text:
    # Safety screen first
    is_safe, message = basic_screen(user_text)
    if not is_safe:
        with st.chat_message("assistant"):
            st.warning(message)
        st.stop()

    with st.chat_message("user"):
        st.markdown(user_text)
    st.session_state.history.append({"role": "user", "content": user_text})

    # Call model (or fallback demo if no key)
    client = get_client()
    if client is None:
        fallback = (
            "Demo mode (no API key found). If this were live, I’d answer with "
            "a concise explanation plus an ethical lens. Add your key to `.env`."
        )
        with st.chat_message("assistant"):
            st.info(fallback)
        st.session_state.history.append({"role": "assistant", "content": fallback})
    else:
        with st.chat_message("assistant"):
            msg = st.empty()
            try:
                resp = client.chat.completions.create(
                    model=get_model(),
                    messages=build_messages(SYSTEM_PROMPT, st.session_state.history[:-1], user_text),
                    temperature=0.4,
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                answer = f"Model error: {e}"
            msg.markdown(answer)
        st.session_state.history.append({"role": "assistant", "content": answer})