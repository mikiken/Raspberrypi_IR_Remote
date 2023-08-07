import os
import subprocess, sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Bot Token と Socket Mode Handler を使ってアプリを初期化
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

DIR_PATH = os.getcwd()
IRRP_PATH = DIR_PATH + '/' + 'irrp.py'
CODES_PATH = DIR_PATH + '/codes'

@app.message("電気ON")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_on', 'switch:on'])
    say("電気をつけました")

@app.message("電気OFF")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_off', 'switch:off'])
    say("電気を消しました")

@app.message("エアコンON")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_on', 'switch:on'])
    say("エアコンをつけました")

@app.message("エアコンOFF")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_off', 'switch:off'])
    say("エアコンを消しました")

@app.message("おはよう")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_on', 'switch:on'])
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_on', 'switch:on'])
    say("電気とエアコンをつけました")

@app.message("おやすみ")
def message_hello(say):
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_off', 'switch:off'])
    subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_off', 'switch:off'])
    say("電気とエアコンを消しました")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()