from flask import Flask, request, abort

# Flaskアプリのインスタンスを作成
app = Flask(__name__)


# '/' という一番シンプルなURLにアクセスがあった時の処理
# methods=["POST"]を追加して、POSTリクエストを受けるけるようにする
@app.route("/callback", methods=["POST"])
def callback():
    # ここから先は今後LINEからの情報を受け取って処理するコードを書く

    # まずはLINEに「正常に受け取った」証明として必ず200　OKを返す
    return "OK", 200


# このファイルが直接実行された場合にのみ、Webサーバーを起動する
if __name__ == "__main__":
    # デバッグモードを有効にしてサーバーを起動
    # ※デバッグモード：コードを変更すると自動で再起動してくれたり、エラー表示が親切になったりする開発用の便利モード
    app.run(debug=True, ssl_context=("cert.pem", "key.pem"))
