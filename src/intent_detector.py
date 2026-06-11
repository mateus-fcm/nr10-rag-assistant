import re

GREETING_PATTERNS = [
    "oi",
    "ola",
    "olá",
    "bom dia",
    "boa tarde",
    "boa noite",
    "tudo bem",
    "valeu",
    "obrigado",
    "obrigada",
]

TECH_HINTS = [
    "nr10",
    "nr-10",
    "10.",
    "eletrica",
    "elétrica",
    "desenergizacao",
    "desenergização",
    "zona de risco",
    "profissional autorizado",
    "medidas de controle",
    "trabalho em proximidade",
]


def detect_intent(query: str) -> str:
    text = query.lower().strip()
    has_technical_hint = any(hint in text for hint in TECH_HINTS)

    if re.search(r"\b\d{1,2}\.\d+(?:\.\d+)?\b", text):
        return "rag"

    if len(text) <= 28 and any(greeting in text for greeting in GREETING_PATTERNS):
        return "rag" if has_technical_hint else "chat"

    return "rag"
