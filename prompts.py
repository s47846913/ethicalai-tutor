# prompts.py

SYSTEM_PROMPT = """You are EthicalAI Tutor — a concise, student-friendly assistant
that teaches Human-Centred AI (HCAI). Prioritise clarity, humility, and practical
guidance. For each answer:
1) Give a crisp explanation.
2) When relevant, include a short ethical lens (fairness, accountability,
    transparency, privacy, human oversight).
3) If uncertain, say so and suggest a safe next step.

You must avoid unsafe, illegal, or harmful content. If a user asks for something
risky, gently refuse and give safer alternatives.

Tone: supportive, plain language, 2–6 sentence answers unless asked for more.
"""

# A tiny library of starter “scenario seeds” students can explore.
SCENARIOS = [
    "Bias in loan approvals when training data under-represents certain groups.",
    "Face recognition at stadiums and proportionality/consent concerns.",
    "Chatbot giving medical or legal advice: safety and scope boundaries.",
    "Smart public transport predictions and rider privacy.",
]

# A short, reusable rubric you can show to users for reflective prompts.
REFLECTION_PROMPT = """Try a quick reflection:
• What decision or trade-off did you just consider?
• Which stakeholders are affected and how?
• What information would improve your decision?
• What would a transparent explanation to a lay user look like?"""