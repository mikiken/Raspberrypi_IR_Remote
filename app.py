import os
import subprocess, sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from irrp import IRRP

# Bot Token と Socket Mode Handler を使ってアプリを初期化
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

DIR_PATH = os.getcwd()
IRRP_PATH = DIR_PATH + '/' + 'irrp.py'
CODES_PATH = DIR_PATH + '/codes'

@app.message("電気ON")
def message_hello(say):
    # subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_on', 'switch:on'])
    ir = IRRP(file=f'{CODES_PATH}/light', no_confirm=True)
    ir.Playback(GPIO=14, ID="switch:on")
    ir.stop()
    say("電気をつけました")

@app.message("電気OFF")
def message_hello(say):
    # subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/light_off', 'switch:off'])
    ir = IRRP(file=f'{CODES_PATH}/light', no_confirm=True)
    ir.Playback(GPIO=14, ID="switch:off")
    ir.stop()
    say("電気を消しました")

@app.message("エアコンON")
def message_hello(say):
    # subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_on', 'switch:on'])
    ir = IRRP(file=f'{CODES_PATH}/aircon', no_confirm=True)
    ir.Playback(GPIO=14, ID="switch:on")
    ir.stop()
    say("エアコンをつけました")

@app.message("エアコンOFF")
def message_hello(say):
    # subprocess.run(['python', IRRP_PATH, '-p', '-g14', '-f', f'{CODES_PATH}/aircon_off', 'switch:off'])
    ir = IRRP(file=f'{CODES_PATH}/aircon', no_confirm=True)
    ir.Playback(GPIO=14, ID="switch:off")
    ir.stop()
    say("エアコンを消しました")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()