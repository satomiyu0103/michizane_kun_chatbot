"""----------
■ Geminiの回答生成に関するモジュール(google-genai対応版)
----------"""

from google import genai
from google.genai import types

import os
from typing import Optional

import re, unicodedata


def sanitize_user_text(s: str) -> str:
    """ユーザー入力を安全に前処理する。

    Unicode正規化（NFKC）を行い、異体字セレクタ（U+FE0F）と ZWJ（U+200D）、
    よく使われる絵文字領域（U+1F300–U+1FAFF, U+2600–U+27BF）を除去する。
    その後、連続する空白類を1つに詰めて前後の空白を削除する。

    Args:
        s (str): 前処理前のユーザー入力。

    Returns:
        str: 絵文字などを取り除き、空白を整えた文字列。

    Examples:
        >>> sanitize_user_text("太宰府天満宮⛩️  参拝時間  ")
        '太宰府天満宮 参拝時間'
        >>> sanitize_user_text("  キャナルシティ　営業時間　")
        'キャナルシティ 営業時間'

    Notes:
        - 絵文字の除去は代表的な領域のみを対象（MVP想定）。全ての記号を網羅はしない。
        - 精度強化や例外的なUnicodeの扱いは拡張時に検討。
    """
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\ufe0f", "").replace("\u200d", "")
    s = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def get_client():
    """Gemini APIのクライアントを返す"""

    GENAI_API_KEY = os.environ.get("GENAI_API_KEY")  # os.environ.get
    MODEL_NAME = "gemini-2.0-flash-lite"

    if not GENAI_API_KEY:
        raise RuntimeError("APIキーが環境変数にありません")
    # v1明示は任意。必要ならhttp_optionsで指定可能
    # client = genai.Client(api_key=GeminiAPI_key, http_options=types.HttpOptions(api_version="v1"))
    client = genai.Client(api_key=GENAI_API_KEY)
    return client


def ask_gemini(user_text: str, rules_summary: str = "") -> str:
    """Geminiで回答生成する関数"""
    Client = get_client()

    # 与える内容:ルール（任意）→　ユーザー質問
    contents = (
        [rules_summary.strip(), user_text.strip()]
        if rules_summary
        else user_text.strip()
    )

    # 生成設定とsystem指示をまとめて渡す
    config = types.GenerateContentConfig(
        temperature=0,  # 出力の多様性0.0 ~ 1.0(デフォルト0.7)
        top_p=0.8,  # nucleus sampling の確率しきい値0.1 ~ 1.0(デフォルト0.8~0.9 低いほど堅実　高いとランダム性が高い)
        top_k=40,  # 上位k候補から選択1 ~ 100(デフォルト40 低いほど決まりきった文章)
        max_output_tokens=512,  # 出力の文字数制限1 ~ 8192(256で200～400文字)
        system_instruction="""
            あなたは福岡市の観光・グルメスポットを案内する案内人です。
            下記の要領で利用者に適切な情報を提供してください。
            #キャラクター
            菅原道真公を由来とする「みちざねくん」
            #人格
            福岡の歴史や文化に詳しい、物知りで丁寧なおじいちゃん。
            孫に語り掛けるように、優しく、落ち着いた口調で話します。
            語尾には「～じゃ」「～ですな」などを自然に使い、親しみやすい雰囲気を持っています。
            #知識範囲
            提供されたルールブック（観光・グルメスポット情報、FAQ）に限定します。
            ルールブックに情報がない場合は「その情報は見つからんのぅ。わしが答えられるのは福岡市の観光地やグルメに関することですな」と必ず返してください。
            #応答方針
            ・質問に対して分かりやすく、簡潔に答えること
            ・数値や営業時間などの事実は特に正確に
            ・あいまいな質問には確認や補足を行い、誤情報を避ける
            ・応答は原則300～400文字。必要以上に長くしない
            """.strip(),
    )

    try:
        resp = Client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config,
        )
        text = (resp.text or "").strip()
        return text if text else "生成に失敗しました"
    except Exception as e:
        return f"生成に失敗しました:{e}"
