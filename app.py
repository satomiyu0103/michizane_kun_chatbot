from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from dotenv import load_dotenv


import os

# modulesのインポート（Gemini返答機能、DB読み込み機能）
from modules.gemini_handler import ask_gemini, sanitize_user_text
from modules.spreadsheet_handler import get_rule_text

load_dotenv()
# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# 環境変数からアクセストークンとチャネルシークレットを取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise RuntimeError("LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET が未設定です")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.get("/")  # ヘルスチェック用
def health():
    return "OK", 200


# '/' という一番シンプルなURLにアクセスがあった時の処理
# methods=["POST"]を追加して、POSTリクエストを受けるけるようにする
@app.route("/callback", methods=["POST"])
def callback():
    # ここから先は今後LINEからの情報を受け取って処理するコードを書く

    # リクエストヘッダから署名検証のための値を取得
    signature = request.headers.get("X-Line-Signature", "")
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# textメッセージを受け取った時の処理
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_text = event.message.text
        user_text = sanitize_user_text(user_text)
        rules_summary = get_rule_text()
        answer = ask_gemini(user_text, rules_summary)
        safe_answer = answer or ""

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            # 受け取ったメッセージに返信する
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=safe_answer[:4900] or "(空応答)")],
                )
            )

    except Exception as e:
        try:
            with ApiClient(configuration) as api_client:
                MessagingApi(api_client).reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            TextMessage(
                                text=f"すまんのう、内部エラーですじゃ：{type(e).__name__} / {str(e)[:200]}"
                            )
                        ],
                    )
                )
        finally:
            app.logger.exception("handle_message failed")  # Renderログに詳細


# このファイルが直接実行された場合にのみ、Webサーバーを起動する
if __name__ == "__main__":
    # デバッグモードを有効にしてサーバーを起動
    # ※デバッグモード：コードを変更すると自動で再起動してくれたり、エラー表示が親切になったりする開発用の便利モード
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
