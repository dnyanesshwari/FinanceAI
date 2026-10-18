"""LLM configuration for the application."""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from app.utils.logger import logger


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class GeminiTextModel:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)

    def invoke(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"temperature": 0.2, "max_output_tokens": 300},
        )
        return {"content": self._extract_text(response)}

    @staticmethod
    def _extract_text(response):
        if hasattr(response, "text") and response.text:
            return response.text
        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            content = getattr(candidate, "content", None)
            if content and hasattr(content, "parts"):
                parts = []
                for part in content.parts:
                    if hasattr(part, "text"):
                        parts.append(part.text)
                    elif isinstance(part, dict) and part.get("text"):
                        parts.append(part["text"])
                if parts:
                    return "".join(parts)
        return str(response)


def _fallback_answer(prompt: str) -> str:
    lower_prompt = prompt.lower()

    if "classify the user query" in lower_prompt:
        query_match = re.search(r"Query:\s*(.+?)\s*$", prompt, re.IGNORECASE | re.DOTALL)
        text = query_match.group(1).lower() if query_match else ""
        if re.search(r"\b(rbi|regulation|regulated|loan|tax|legal|digital lending|sebi)\b", text):
            return "regulation"
        if re.search(r"\b(budget|plan|save|invest|spend|emergency|goal|retire)\w*\b", text):
            return "planning"
        return "general"

    if "calculation type:" in lower_prompt or "result:" in lower_prompt:
        calc_type_match = re.search(r"Calculation type:\s*(.+?)\n", prompt, re.DOTALL)
        result_match = re.search(r"Result:\s*(.+?)\n", prompt, re.DOTALL)
        calc_type = (calc_type_match.group(1).strip() if calc_type_match else "financial calculation")
        result = (result_match.group(1).strip() if result_match else "the calculated value")
        return (
            f"Using the verified calculator, the {calc_type} result is {result}. "
            "This value is based on the inputs provided in the request."
        )

    if "context:" in lower_prompt and "question:" in lower_prompt:
        context_match = re.search(
            r"Context:[ \t]*\r?\n(.*?)(?:\r?\n[ \t]*Question:|$)",
            prompt,
            re.IGNORECASE | re.DOTALL,
        )
        context = context_match.group(1).strip() if context_match else "No context was returned."
        if not context:
            question_match = re.search(
                r"Question:[ \t]*\r?\n(.*?)(?:\r?\n[ \t]*Answer:|$)",
                prompt,
                re.IGNORECASE | re.DOTALL,
            )
            question = question_match.group(1).strip() if question_match else ""
            if re.fullmatch(r"(?:hi|hii|hello|hey|good morning|good afternoon|good evening)[!. ]*", question, re.IGNORECASE):
                return "Hi! I can help with EMI and interest calculations, financial regulations, or budgeting and savings plans. What would you like to work on?"
            if question:
                return "I can help with financial calculations, regulations, and planning. Could you add a little more detail to your question?"
            return "I couldn't find relevant source material for that question. Please try rephrasing it."
        summary = " ".join(context.split())
        if len(summary) > 220:
            summary = summary[:220] + "..."
        return f"Based on the available source material: {summary}"

    return (
        "The AI model is temporarily unavailable, but the app is still running. "
        "Please retry the request or use a calculator endpoint for numeric results."
    )


def get_llm():
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        raise RuntimeError("No API key configured. Add GEMINI_API_KEY or GOOGLE_API_KEY to Backend/.env.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return GeminiTextModel(model_name=model, api_key=gemini_key)


def invoke_text(llm, prompt: str) -> str:
    """Normalize chat-model responses to the text interface used by the app."""
    try:
        response = llm.invoke(prompt)
    except Exception as exc:
        logger.exception("Gemini request failed; using local fallback: %s", exc)
        return _fallback_answer(prompt)

    content = response.get("content", "") if isinstance(response, dict) else getattr(response, "content", response)
    if isinstance(content, list):
        content = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    text = str(content).strip()
    if not text or text.lower() in {"none", ""}:
        logger.warning("Gemini returned an empty response; using local fallback")
        return _fallback_answer(prompt)
    return text
