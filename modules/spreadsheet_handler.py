"""---------
■ DBスプシを読み込みルールテキストを作成するモジュール
---------"""

import pandas as pd
import os


def csv_url(sheet_name: str) -> str:
    """スプレッドシートを読み込むためのURLを作成する

    Args:
        sheet_name (str): Databaseのあるスプシのシート名

    Returns:
        str: 読み込み用URL
    """
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
    """DB保存スプレッドシートをDataFrameとして読み込む

    Returns:
        pandas.core.frame.DataFrame: それぞれのDBシートをDataFrameとして読み込む
    """
    # 読み込み用URLを作成する
    url_faq = csv_url("faq")
    url_spots = csv_url("spots")
    url_tags = csv_url("tags")
    url_categories = csv_url("categories")
    # スプシをcsvで読み込みDataFrameへ変換する
    df_faq = pd.read_csv(url_faq)
    df_spots = pd.read_csv(url_spots)
    df_tags = pd.read_csv(url_tags)
    df_categories = pd.read_csv(url_categories)
    return df_faq, df_spots, df_tags, df_categories


def get_rule_text():
    """DataFrameとして読み込んだDBをstr型に変換し、
    textとして全文結合する

    Returns:
        str: Geminiに渡すルールテキスト
    """
    df_faq, df_spots, df_tags, df_categories = load_spresheet()
    text_faq = df_faq.to_string(index=False)
    text_spots = df_spots.to_string(index=False)
    text_tags = df_tags.to_string(index=False)
    text_categories = df_categories.to_string(index=False)
    text = text_faq + "\n" + text_spots + "\n" + text_tags + "\n" + text_categories
    return text
