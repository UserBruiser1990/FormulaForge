import re

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"


def _clean_code(response: str) -> str:
    """Remove optional markdown fences that models sometimes add to code."""
    return re.sub(r"^```(?:\w+)?\s*|\s*```$", "", response.strip()).strip()


class OllamaServiceError(RuntimeError):
    """Raised when Ollama cannot generate a response."""


def generate_formula(prompt: str) -> str:
    """Send a formula request to Ollama and return the generated text."""
    request_prompt = (
        "You generate Excel formulas. Convert the user's request into one valid "
        "Excel formula. Return only the formula, with no explanation or markdown.\n\n"
        f"User request: {prompt}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": request_prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise OllamaServiceError("Unable to connect to Ollama.") from exc
    except ValueError as exc:
        raise OllamaServiceError("Ollama returned invalid JSON.") from exc

    generated_text = result.get("response")
    if not isinstance(generated_text, str) or not generated_text.strip():
        raise OllamaServiceError("Ollama returned an empty response.")

    return generated_text.strip()


def explain_formula(formula: str) -> str:
    """Send an Excel formula to Ollama and return a plain-English explanation."""
    request_prompt = (
        "You explain Excel formulas in plain English for non-technical users. "
        "Describe what the formula does, including important criteria or ranges. "
        "Do not use markdown.\n\n"
        f"Excel formula: {formula}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": request_prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise OllamaServiceError("Unable to connect to Ollama.") from exc
    except ValueError as exc:
        raise OllamaServiceError("Ollama returned invalid JSON.") from exc

    explanation = result.get("response")
    if not isinstance(explanation, str) or not explanation.strip():
        raise OllamaServiceError("Ollama returned an empty response.")

    return explanation.strip()


def fix_formula(formula: str) -> str:
    """Send a broken Excel formula to Ollama and return a corrected formula."""
    request_prompt = (
        "You repair Excel formulas. Correct the user's broken formula while "
        "preserving its intended purpose. Return only one valid Excel formula, "
        "with no explanation or markdown.\n\n"
        f"Broken Excel formula: {formula}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": request_prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise OllamaServiceError("Unable to connect to Ollama.") from exc
    except ValueError as exc:
        raise OllamaServiceError("Ollama returned invalid JSON.") from exc

    corrected_formula = result.get("response")
    if not isinstance(corrected_formula, str) or not corrected_formula.strip():
        raise OllamaServiceError("Ollama returned an empty response.")

    return corrected_formula.strip()


def generate_vba(prompt: str) -> str:
    """Send a VBA request to Ollama and return the generated macro."""
    request_prompt = (
        "You generate Excel VBA macros. Convert the user's request into safe, "
        "valid VBA code. Return only the code, with no markdown fences or explanation.\n\n"
        f"User request: {prompt}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": request_prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise OllamaServiceError("Unable to connect to Ollama.") from exc
    except ValueError as exc:
        raise OllamaServiceError("Ollama returned invalid JSON.") from exc

    code = result.get("response")
    if not isinstance(code, str) or not code.strip():
        raise OllamaServiceError("Ollama returned an empty response.")

    return _clean_code(code)


def generate_power_query(prompt: str) -> str:
    """Send a Power Query request to Ollama and return M code."""
    request_prompt = (
        "You generate Power Query M code. Convert the user's request into valid "
        "M code. Return only the code, with no markdown fences or explanation.\n\n"
        f"User request: {prompt}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": request_prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise OllamaServiceError("Unable to connect to Ollama.") from exc
    except ValueError as exc:
        raise OllamaServiceError("Ollama returned invalid JSON.") from exc

    code = result.get("response")
    if not isinstance(code, str) or not code.strip():
        raise OllamaServiceError("Ollama returned an empty response.")

    return _clean_code(code)