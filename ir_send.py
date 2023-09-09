from irrp import IRRP
import json
import io
import encode

LED_PIN = 14


def ir_send(decoded_code: str):
    ir_code_json = io.StringIO(json.dumps({"ir_code": decoded_code}))
    ir = IRRP(no_confirm=True)
    ir.Playback(GPIO=LED_PIN, ID="ir_code", file_object=ir_code_json)
    ir.stop()

def main():
    ir_send(encode.encode_ir_signal("AEHA", encode.encode_mitsubishi_aircon("on", "ac_move_eye", 26), 425, 2))

if __name__ == "__main__":
    main()
