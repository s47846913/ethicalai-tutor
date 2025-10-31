# app.py
import os  # Import OS module for environment variables
import streamlit as st  # Import Streamlit for web app interface
from prompts import SYSTEM_PROMPT, SCENARIOS, REFLECTION_PROMPT  # Import prompts for chatbot context and scenarios
from utils import get_client, get_model, build_messages  # Import utility functions for model interaction
from safety import basic_screen  # Import safety screening to ensure ethical responses
from lessons import LESSONS  # Import mini-lessons content for educational purposes
from logging_utils import log_event  # Import logging utility for tracking interactions

####################################################################
# Initialize Streamlit page configuration for usability and clarity
# This sets the page title, icon, and layout to enhance user experience
####################################################################
st.set_page_config(page_title="EthicalAI Tutor", page_icon="🤖", layout="centered")  # Configure Streamlit page with title, icon, and layout

####################################################################
# Render the main interface components including title, caption,
# and options for explanation to promote transparency and user control
####################################################################
st.title("🤖 EthicalAI Tutor")  # Display main title of the app
st.caption("Level 6 project — Generative AI educational chatbot for HCAI")  # Caption describing the app's educational purpose
explain = st.checkbox("Explain steps (high-level rationale)", value=True)  # Checkbox for enabling explanation of AI reasoning (HCAI clarity)

####################################################################
# Sidebar provides contextual information, scenario ideas, reflection
# templates, mini-lessons, and model info to support user education
# and promote accountability and informed engagement with the AI
####################################################################
with st.sidebar:  # Sidebar for additional info and controls
    st.subheader("About")  # Sidebar section header
    st.write(
        "This chatbot demonstrates Human-Centred AI principles: clarity, "
        "explanations, and safe responses. Try asking about fairness, bias, "
        "privacy, transparency, or accountability."
    )  # Description emphasizing HCAI principles and ethical topics
    st.markdown("**Scenario ideas**")  # Header for scenario suggestions
    for s in SCENARIOS:  # Loop through predefined ethical scenarios
        st.markdown(f"- {s}")  # Display each scenario as a bullet point
    st.divider()  # Visual divider for UI clarity
    st.markdown("**Quick reflection template**")  # Header for reflection prompt
    st.code(REFLECTION_PROMPT, language="markdown")  # Show reflection prompt code snippet for user guidance
    st.subheader("Mini-Lessons")  # Section header for educational lessons
    selected = st.selectbox("Browse a topic", ["(none)"] + list(LESSONS.keys()))  # Dropdown to select mini-lesson topics
    if selected != "(none)":  # If a lesson is selected
        st.markdown(f"**Summary:** {LESSONS[selected]['summary']}")  # Show lesson summary
        st.markdown(f"**Example:** {LESSONS[selected]['example']}")  # Show example illustrating the lesson
        st.markdown("**Reflect:**")  # Prompt reflection questions
        for q in LESSONS[selected]["reflection"]:  # Loop through reflection questions
            st.markdown(f"- {q}")  # Display each question as bullet
    st.divider()  # UI divider for separation
    st.divider()  # Additional divider for clarity
    st.markdown("**Model**")  # Section header for model info
    st.write(os.getenv("OPENAI_MODEL", "gpt-4o-mini"))  # Display current model from environment or default
    st.markdown("Set in `.env` → `OPENAI_MODEL`.")  # Instruction for changing model via environment variable

####################################################################
# Initialize or retrieve chat history from Streamlit session state
# to maintain conversational context and support accountability
####################################################################
if "history" not in st.session_state:  # Initialize chat history in session state if not present
    st.session_state.history = []  # Empty list to store conversation turns

####################################################################
# Display the chat conversation history to ensure transparency 
# and continuity in the user-AI interaction
####################################################################
# Chat window
for m in st.session_state.history:  # Iterate through chat history messages
    with st.chat_message(m["role"]):  # Display each message with correct role (user/assistant)
        st.markdown(m["content"])  # Render message content in markdown

####################################################################
# Handle new user input with safety screening to uphold ethical
# standards and prevent harmful or unethical interactions
####################################################################
user_text = st.chat_input("Ask about HCAI — e.g., fairness in model design")  # Input box for user queries on HCAI topics
if user_text:  # If user has entered text
    # Safety screen first
        is_safe, message = basic_screen(user_text)  # Run safety checks to prevent harmful or unethical inputs
        if not is_safe:  # If input fails safety screening
            with st.chat_message("assistant"):  # Show warning message as assistant response
                st.warning(message)  # Display safety warning
            st.stop()  # Halt further processing to maintain safe interaction

        ####################################################################
        # Append user message to chat history and log the event for 
        # transparency and accountability in interactions
        ####################################################################
        with st.chat_message("user"):  # Display user's message in chat
            st.markdown(user_text)  # Render user input in markdown
        st.session_state.history.append({"role": "user", "content": user_text})  # Append user message to history
        log_event("user", user_text, explain, selected if selected != "(none)" else None)  # Log user input event with context

        ####################################################################
        # Attempt to get AI response using the configured model client,
        # fallback to demo mode if API key is missing to maintain usability
        ####################################################################
        # Call model (or fallback demo if no key)
        client = get_client()  # Initialize API client for language model
        if client is None:  # If no API key or client is unavailable
            fallback = (
            "Demo mode (no API key found). If this were live, I’d answer with "
            "a concise explanation plus an ethical lens. Add your key to `.env`."
                )  # Inform user that demo mode is active without live AI responses
            with st.chat_message("assistant"):  # Show fallback message as assistant
                st.info(fallback)  # Display info box with fallback message
            st.session_state.history.append({"role": "assistant", "content": fallback})  # Append fallback to history
        else:  # If client is available, proceed with AI response
            with st.chat_message("assistant"):  # Prepare assistant message container
                msg = st.empty()  # Placeholder for streaming or updating message
            try:
                extra_hint = "User enabled Explain steps." if explain else "User disabled Explain steps."  # Indicate explanation preference
                resp = client.chat.completions.create(
                    model=get_model(),  # Select model based on environment or defaults
                    messages=build_messages(SYSTEM_PROMPT + f"\n{extra_hint}", st.session_state.history[:-1], user_text),  # Build prompt with system context and conversation history
                    temperature=0.4,  # Set response creativity level (lower for clarity)
                )
                answer = resp.choices[0].message.content  # Extract assistant's reply text
            except Exception as e:  # Handle exceptions from API call
                answer = f"Model error: {e}"  # Return error message as assistant response
            msg.markdown(answer)  # Display assistant's answer in markdown
        st.session_state.history.append({"role": "assistant", "content": answer})  # Append assistant response to history
        log_event("assistant", answer, explain, selected if selected != "(none)" else None)  # Log assistant's response with context