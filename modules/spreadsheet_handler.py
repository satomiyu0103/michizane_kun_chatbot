import pandas as pd
import os


def csv_url(sheet_name):
    # load_dotenv()
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    GID = {
        "faq": 1932958690,
        "spots": 0,
        "tags": 1863403900,
        "categories": 88251615,
    }
    return f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID[sheet_name]}"


def load_spresheet():
    url_faq = csv_url("faq")
    url_spots = csv_url("spots")
    url_tags = csv_url("tags")
    url_categories = csv_url("categories")
    df_faq = pd.read_csv(url_faq)
    df_spots = pd.read_csv(url_spots)
    df_tags = pd.read_csv(url_tags)
    df_categories = pd.read_csv(url_categories)
    return df_faq, df_spots, df_tags, df_categories


def get_rule_text():
    df_faq, df_spots, df_tags, df_categories = load_spresheet()
    text_faq = df_faq.to_string(index=False)
    text_spots = df_spots.to_string(index=False)
    text_tags = df_tags.to_string(index=False)
    text_categories = df_categories.to_string(index=False)
    text = text_faq + "\n" + text_spots + "\n" + text_tags + "\n" + text_categories
    return text
