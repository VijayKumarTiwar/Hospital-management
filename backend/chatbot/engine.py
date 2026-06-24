"""
Rule-based symptom-checker engine.

This is intentionally simple (keyword matching against the SymptomEntry
knowledge base) so it's easy to understand and extend. Swap `get_response()`
internals for a real NLP/LLM call later without touching the views/serializers.
"""

from .models import SymptomEntry

URGENCY_ORDER = {"low": 0, "medium": 1, "high": 2, "emergency": 3}

FALLBACK_RESPONSE = {
    "reply": (
        "I couldn't match specific symptoms in what you described. "
        "Please consult a doctor for an accurate diagnosis, or describe your "
        "symptoms in more detail (e.g. 'I have a fever and a cough')."
    ),
    "urgency": "low",
    "matched_keywords": [],
    "suggested_specialization": None,
}


def get_response(message: str) -> dict:
    """
    Matches keywords from the SymptomEntry table against the user's message.
    Returns the highest-urgency match along with combined advice.
    """
    text = message.lower()
    entries = SymptomEntry.objects.select_related("suggested_specialization").all()

    matches = [entry for entry in entries if entry.keyword.lower() in text]

    if not matches:
        return FALLBACK_RESPONSE

    matches.sort(key=lambda e: URGENCY_ORDER.get(e.urgency, 0), reverse=True)
    top_match = matches[0]

    combined_advice = " ".join(dict.fromkeys(m.advice for m in matches))  # dedupe, preserve order

    return {
        "reply": combined_advice,
        "urgency": top_match.urgency,
        "matched_keywords": [m.keyword for m in matches],
        "suggested_specialization": (
            top_match.suggested_specialization.name if top_match.suggested_specialization else None
        ),
    }


DEFAULT_SYMPTOM_SEED = [
    {"keyword": "fever", "advice": "Stay hydrated and rest. If fever exceeds 39°C (102°F) or lasts more than 3 days, see a doctor.", "urgency": "medium"},
    {"keyword": "headache", "advice": "Mild headaches often resolve with rest and hydration. Persistent or severe headaches need evaluation.", "urgency": "low"},
    {"keyword": "chest pain", "advice": "Chest pain can indicate a serious condition. Please seek emergency care immediately.", "urgency": "emergency"},
    {"keyword": "shortness of breath", "advice": "Difficulty breathing can be serious. Seek immediate medical attention.", "urgency": "emergency"},
    {"keyword": "cough", "advice": "A cough lasting more than 2 weeks, or accompanied by blood, should be evaluated by a doctor.", "urgency": "low"},
    {"keyword": "rash", "advice": "Note when the rash appeared and any new products/foods. See a doctor if it spreads or is painful.", "urgency": "low"},
    {"keyword": "abdominal pain", "advice": "Severe or persistent abdominal pain should be evaluated promptly.", "urgency": "high"},
    {"keyword": "vomiting", "advice": "Stay hydrated with small sips of fluids. Seek care if vomiting persists beyond 24 hours or contains blood.", "urgency": "medium"},
]


def seed_symptoms():
    """Idempotently populate the knowledge base with default entries."""
    created = 0
    for item in DEFAULT_SYMPTOM_SEED:
        _, was_created = SymptomEntry.objects.get_or_create(
            keyword=item["keyword"],
            defaults={"advice": item["advice"], "urgency": item["urgency"]},
        )
        created += int(was_created)
    return created
