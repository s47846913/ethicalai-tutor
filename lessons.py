# lessons.py
LESSONS = {
    "Fairness 101": {
        "summary": "Sources of bias (data, labels, deployment). Mitigations: re-sampling, re-weighting, audits.",
        "example": "Loan approvals under-represent Group A. Try stratified sampling + threshold analysis.",
        "reflection": ["Whose error matters most?", "What metric is fair in this context?"]
    },
    "Transparency & Explainability": {
        "summary": "Explain the *what* and *why*, not internal weights. Prefer plain-language rationales.",
        "example": "Show feature attributions at a high level; disclose uncertainty.",
        "reflection": ["What would a layperson need to trust this?"]
    },
    "Privacy & Data Minimisation": {
        "summary": "Collect the least data needed; prefer aggregation or differential privacy.",
        "example": "Smart transport prediction with anonymised, aggregated tap-on data.",
        "reflection": ["What happens if data leaks?"]
    }
}