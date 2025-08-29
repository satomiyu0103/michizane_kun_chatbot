from dotenv import load_dotenv
from modules.test_gemini_handler import _get_model, ask_gemini
from modules.spreadsheet_handler import get_rule_text

DEFAULT_USER_TEXT = """
福岡の有名グルメを一つ教えて
    """


def main(user_text: str = DEFAULT_USER_TEXT):
    model = _get_model()
    rules = get_rule_text()
    reply = ask_gemini(model, user_text, rules_summary=rules)
    print(reply)


if __name__ == "__main__":
    main(DEFAULT_USER_TEXT)
