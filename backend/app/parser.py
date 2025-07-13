import os
import json
import logging
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Initialize Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

logger = logging.getLogger(__name__)

# Gemini model initialization
model = genai.GenerativeModel("models/gemini-1.5-flash")

def extract_with_ai(description: str) -> Dict[str, List[str] or str]:
    if not description.strip():
        print("[extract_with_ai] Empty description received")
        return {"services": [], "summary": ""}

    prompt = f"""
You are a cloud architecture expert.
Given the following AWS architecture description, extract:
1. A list of AWS cloud services mentioned or implied (e.g., EC2, S3, Lambda).
2. A short one-line summary of the architecture's purpose.

Description:
\"\"\"{description}\"\"\"

Respond only in valid JSON:
{{
  "services": ["..."],
  "summary": "..."
}}
"""

    print("[extract_with_ai] Sending prompt to Gemini:")
    print(prompt)

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        print("[extract_with_ai] Raw response content:")
        print(content)

        # Strip markdown code block if present (```json ... ```)
        if content.startswith("```"):
            lines = content.splitlines()
            # Remove first line if it starts with ```
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it is ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()
            print("[extract_with_ai] Stripped markdown code block:")
            print(content)

        # Parse JSON now
        result = json.loads(content)

        # Defensive validation
        if not isinstance(result, dict):
            raise ValueError("Gemini response is not a JSON object")
        services = result.get("services", [])
        summary = result.get("summary", "")

        if not isinstance(services, list):
            services = []
        if not isinstance(summary, str):
            summary = ""

        print(f"[extract_with_ai] Parsed services: {services}")
        print(f"[extract_with_ai] Parsed summary: {summary}")

        return {"services": services, "summary": summary}

    except Exception as e:
        logger.error("[Gemini parsing failed]", exc_info=e)
        print(f"[extract_with_ai] Exception parsing Gemini response: {e}")
        return {"services": [], "summary": ""}

def parse_architecture_data(raw_data: List[dict]) -> List[dict]:
    parsed = []
    for i, item in enumerate(raw_data):
        description = item.get("description", "")
        print(f"[parse_architecture_data] Parsing item {i} - name: {item.get('name', 'Unnamed Architecture')}")
        ai_output = extract_with_ai(description)
        parsed_item = {
            "name": item.get("name", "Unnamed Architecture"),
            "description": description,
            "summary": ai_output.get("summary", ""),
            "services": ai_output.get("services", []),
            "category": item.get("category")
        }
        print(f"[parse_architecture_data] Parsed item {i}: {parsed_item}")
        parsed.append(parsed_item)
    return parsed
