from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

# 正規表現
import re
# しりとり用
from functions.judge import iskatahira, judger
# ヘルプ用
from functions.help import help

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# しりとり
word_list=[]

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received = event.message.text
    if re.match('\!.*', received):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=help(received))
        )
    else:
        word = received
        global word_list
        status = judger(word=word, word_list=word_list)
        if status == 0:
            msg = "accepted"
        elif status == 1:
            msg = "GAME OVER! 語尾が「ん」です"
        elif status == 2:
            msg = "前の単語の語尾と一致していません"
        elif status == 3:
            msg = "GAME OVER! 既に使用された語です"
        elif status == 4:
            msg = "ひらがなで入力してください"
        # ゲームオーバーだったらリセット
        if status in [1,3]:
            word_list = []
            msg = msg + '\n' + "リセットされました。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg + '\n' + "Your input was: " + event.message.text)
        )


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)