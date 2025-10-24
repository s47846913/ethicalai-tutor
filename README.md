# EthicalAI Tutor (Level 6)

An educational chatbot that uses a generative model to teach Human-Centred AI (HCAI) concepts
with a lightweight ethics/safety layer and reflective prompts.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env  # paste your OpenAI key and model
streamlit run app.py