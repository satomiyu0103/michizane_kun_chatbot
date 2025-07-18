from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageReguest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# 環境変数からアクセストークンとチャネルシークレットを取得
LINE_CANNEL_ACCESS_TOKEN = os.environ.get("LINE_CANNEL_ACCESS_TOKEN")
LINE_CANNEL_SECRET = os.environ.get("LINE_CANNEL_SECRET")

configuration = Configuration(access_token=LINE_CANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CANNEL_SECRET)


# '/' という一番シンプルなURLにアクセスがあった時の処理
# methods=["POST"]を追加して、POSTリクエストを受けるけるようにする
@app.route("/callback", methods=["POST"])
def callback():
    # ここから先は今後LINEからの情報を受け取って処理するコードを書く

    # リクエストヘッダから署名検証のための値を取得
    signature = request.headers["X-Line-Signature"]

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
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # 受け取ったメッセージをそのまま返信する
        line_bot_api.reply_message_with_http_info(
            ReplyMessageReguest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )


# このファイルが直接実行された場合にのみ、Webサーバーを起動する
if __name__ == "__main__":
    # デバッグモードを有効にしてサーバーを起動
    # ※デバッグモード：コードを変更すると自動で再起動してくれたり、エラー表示が親切になったりする開発用の便利モード
    app.run(debug=True, ssl_context=("cert.pem", "key.pem"))
