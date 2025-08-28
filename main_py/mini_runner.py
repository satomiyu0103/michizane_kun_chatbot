from dotenv import load_dotenv
from modules.test_gemini_handler import _get_model, ask_gemini

user_text = """
福岡の有名グルメを一つ教えて
    """
rules_summary = ""


def main(user_text, rules_summary):
    model = _get_model()
    text = ask_gemini(model, user_text, rules_summary)
    print(text)


if __name__ == "__main__":
    run(user_text, rules_summary)
