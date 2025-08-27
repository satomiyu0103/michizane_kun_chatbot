from dotenv import load_dotenv
from modules.test_gemini_handler import get_keys, _get_model, ask_gemini

user_text = """
福岡の有名グルメと言えば？
    """
rules_summary = ""


def run(user_text, rules_summary):
    GENAI_API_KEY, MODEL_NAME = get_keys()
    global _model
    if _model is None:
        _model = _get_model(GENAI_API_KEY, MODEL_NAME)
    ask_gemini(_model, user_text, rules_summary)


if __name__ == "__main__":
    run(user_text, rules_summary)
