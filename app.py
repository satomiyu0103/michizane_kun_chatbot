from flask import Flask

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# '/' という一番シンプルなURLにアクセスがあった時の処理
@app.route('/')
def hello():
    # 「Hello, Michizane-kun!」という文字を返す
    return 'Hello, Michizane-kun!'

# このファイルが直接実行された場合にのみ、Webサーバーを起動する
if __name__ == '__main__':
    # デバッグモードを有効にしてサーバーを起動
    # ※デバッグモード：コードを変更すると自動で再起動してくれたり、エラー表示が親切になったりする開発用の便利モード
    app.run(debug=True)