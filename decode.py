import json
import argparse


# 入力された赤外線LEDの点灯・消灯時間を1周期の時間で割って、正規化する
def normalize(code, T=425):
    normalized_code = []
    frame = []
    for i in range(0, len(code)):
        period = round(code[i] / T)
        # Trailer(Frame終端)の場合
        if period > 8:
            normalized_code.append(frame)
            frame = []
        else:
            frame.append(period)
    normalized_code.append(frame)
    return normalized_code


# AEHAフォーマットに従って、信号をdecodeする
def decode(normalized_code):
    decoded_code = []
    data_frame = ""
    for frame in normalized_code:
        for i in range(0, len(frame) - 1, 2):
            # Leader
            if frame[i] == 8 and frame[i + 1] == 4:
                continue
            # 0 (Data bit)
            elif frame[i] == 1 and frame[i + 1] == 1:
                data_frame += "0"
            # 1 (Data bit)
            elif frame[i] == 1 and frame[i + 1] == 3:
                data_frame += "1"
            else:
                raise ("Unabled to decode.")
        decoded_code.append(data_frame)
        data_frame = ""

    assert all(
        df == decoded_code[0] for df in decoded_code
    ), "Each data frame is not identical."

    return decoded_code[0], len(decoded_code)


def parse_decoded_code(decoded_code):
    customer_code1 = int(decoded_code[7::-1], 2)
    customer_code2 = int(decoded_code[15:7:-1], 2)
    parity_code = int(decoded_code[19:15:-1], 2)
    data0 = int(decoded_code[23:19:-1], 2)
    decoded_code = decoded_code[24:]
    data = []
    while len(decoded_code) > 0:
        data.append(int(decoded_code[7::-1], 2))
        decoded_code = decoded_code[8:]
    data.insert(0, data0)

    frame = {
        "customer_code1": customer_code1,
        "customer_code2": customer_code2,
        "parity_code": parity_code,
        "data": data,
    }

    return frame


def analyze_ir_signal(code) -> None:
    normalized_code = normalize(code)
    decoded_code = decode(normalized_code)[0]
    return parse_decoded_code(decoded_code)


def main() -> None:
    # 引数をパース フォーマットはirrp.pyと同じ
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--file", help="Filename", required=True)
    arg_parser.add_argument("id", nargs="+", type=str, help="IR codes")
    args = arg_parser.parse_args()

    with open(args.file, "r") as f:
        records = json.load(f)

    # 各引数の表す信号に対してdecodeする
    for arg in args.id:
        if arg in records:
            code = records[arg]
            analyze_ir_signal(code)
        else:
            raise (f"Can't find '{arg}' in '{f}'.")


if __name__ == "__main__":
    main()
