import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def analyze_ticket(title: str, description: str) -> dict:
    """
    Returns a dict:
    {
      "summary": "...",
      "priority": "LOW|MEDIUM|HIGH",
      "draft_reply": "..."
    }
    """
    llm = ChatOpenAI(model=MODEL, temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an IT support triage assistant. "
                "Return ONLY valid JSON. No markdown, no extra text.",
            ),
            (
                "user",
                """
Analyze this support ticket and output JSON with:
- summary: 1-2 sentences
- priority: one of LOW, MEDIUM, HIGH
- draft_reply: a helpful short reply (2-5 sentences)

Ticket title: {title}
Ticket description: {description}

Return format (exact keys):
{{
  "summary": "...",
  "priority": "LOW|MEDIUM|HIGH",
  "draft_reply": "..."
}}
""",
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"title": title, "description": description})

    # result.content should be JSON text
    text = result.content.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # fallback: try to extract JSON between first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            data = json.loads(text[start : end + 1])
        else:
            raise

    # minimal validation
    summary = str(data.get("summary", "")).strip()
    priority = str(data.get("priority", "")).strip().upper()
    draft_reply = str(data.get("draft_reply", "")).strip()

    if priority not in {"LOW", "MEDIUM", "HIGH"}:
        priority = "MEDIUM"

    return {
        "summary": summary,
        "priority": priority,
        "draft_reply": draft_reply,
    }