from modules.gemini_handler import ask_gemini
from modules.spreadsheet_handler import get_rule_text

DEFAULT_USER_TEXT = """
福岡の有名グルメを一つ教えて
    """


def main(user_text: str = DEFAULT_USER_TEXT):
    rules = get_rule_text()
    reply = ask_gemini(user_text, rules_summary=rules)
    print(reply)


if __name__ == "__main__":
    main(DEFAULT_USER_TEXT)
