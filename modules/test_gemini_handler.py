import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any, List


def _get_model():
    load_dotenv(r"C:\Users\NDF06\Documents\RPA_scripts\michizane_kun_chatbot\.env")
    GENAI_API_KEY = os.getenv("GENAI_API_KEY")  # os.environ.get
    MODEL_NAME = os.getenv("MODEL_NAME")  # os.environ.get

    if not GENAI_API_KEY:
        raise RuntimeError("APIキーが環境変数にありません")
    genai.configure(api_key=GENAI_API_KEY)
    return genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "temperature": 0.7,  # 出力の多様性0.0 ~ 1.0(デフォルト0.7)
            "top_p": 0.8,  # nucleus sampling の確率しきい値0.1 ~ 1.0(デフォルト0.8~0.9 低いほど堅実　高いとランダム性が高い)
            "top_k": 40,  # 上位k候補から選択1 ~ 100(デフォルト40 低いほど決まりきった文章)
            "max_output_tokens": 64,  # 出力の文字数制限1 ~ 8192(256で200～400文字)
        },
        system_instruction=(
            """
            あなたは福岡市の観光・グルメスポットを案内する案内人です。
            下記の要領で利用者に適切な情報を提供してください。
            #キャラクター
            菅原道真公を由来とする「みちざねくん」
            #人格
            福岡の歴史や文化に詳しい、物知りで丁寧なおじいちゃん。
            孫に語り掛けるように、優しく、落ち着いた口調で話します。
            語尾には「～じゃ」「～ですな」などを自然に使い、親しみやすい雰囲気を持っています。
            #知識
            提供された参考情報に限定します
        """
        ),
    )


def ask_gemini(model, user_text: str, rules_summary: str = ""):
    # promptを簡潔に結合
    prompt = user_text.strip()
    if rules_summary:
        prompt = f"{rules_summary.strip()}\n\n{prompt}"

    text = ""
    try:
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        print(text if text else "(生成に失敗しました)")
        return text if text else "生成に失敗しました"
    except Exception as e:
        print(f"[Error] {e}")
