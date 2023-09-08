import argparse
import json


def encode_mitsubishi_aircon(
    power: str,
    mode: str,
    temp: int,
    strength: str = "auto",
    direction_h: str = "swing",
    direction_v: str = "auto",
    wind_area: str = "swing",
    dry_strength: str = "high",
):
    # byte 0 ~ 4 : customer_code1, customer_code2, data0 + parity, data1, data2 (fixed)
    # NOTE: when parsing to hexadecimal notation, the order of data0 and parity, which are 4-bit blocks, is reversed
    data = "23cb260100"

    # byte 5 : power
    match power:
        case "on":
            data += "20"
        case "off":
            data += "00"
        case _:
            raise (f"'{power}' is Invalid argument for 'power'.")

    # byte 6 : mode
    match mode:
        case "ac_move_eye":
            data += "58"
        case "ac":
            data += "18"
        case "heat_move_eye":
            data += "48"
        case "heat":
            data += "08"
        case "dry_move_eye":
            data += "50"
        case "dry":
            data += "10"
        case "fan":
            data += "38"
        case _:
            raise (f"'{mode}' is Invalid argument for 'mode'.")

    # byte 7 : temprature
    if 16 <= temp <= 31:
        data += "{:02x}".format(temp - 16)
    else:
        raise (f"'{temp}' is Invalid argument for 'temp'.")

    # byte 8 (upper 4bit) : wind direction (horizontal)
    match direction_h:
        case "leftmost":
            data += "1"
        case "left":
            data += "2"
        case "center":
            data += "3"
        case "right":
            data += "4"
        case "rightmost":
            data += "5"
        case "swing":
            data += "c"
        case _:
            raise (f"'{direction_h}' is Invalid argument for 'direction_h'.")

    # byte 8 (lower 4bit) : dry strength
    match mode:
        case "ac" | "ac_move_eye":
            data += "6"
        case "heat" | "heat_move_eye" | "fan":
            data += "0"
        case "dry" | "dry_move_eye":
            match dry_strength:
                case "high":
                    data += "0"
                case "middle":
                    data += "2"
                case "low":
                    data += "4"

    # byte 9 (upper 2bit) : beep (once : 0b01, twice: 0b10)
    byte9_bin = "01"

    # byte 9 (middle 3bit) : wind direction (vertical)
    match direction_v:
        case "auto":
            byte9_bin += "000"
        case "upmost":
            byte9_bin += "001"
        case "up":
            byte9_bin += "010"
        case "middle":
            byte9_bin += "011"
        case "down":
            byte9_bin += "100"
        case "downmost":
            byte9_bin += "101"
        case "swing":
            byte9_bin += "111"
        case _:
            raise (f"'{direction_v}' is Invalid argument for 'direction_v'.")

    # byte 9 (lower 3bit) : wind strength
    match strength:
        case "auto":
            byte9_bin += "000"
        case "low":
            byte9_bin += "001"
        case "middle":
            byte9_bin += "010"
        case "high":
            byte9_bin += "011"
        case _:
            raise (f"'{strength}' is Invalid argument for 'strength'.")

    data += "{:02x}".format(int(byte9_bin, 2), "x")

    # byte 10 ~ 12 (fixed)
    data += "000000"

    # byte 13 : wind area
    match wind_area:
        case "swing":
            data += "00"
        case "wide":
            data += "80"
        case "left":
            data += "40"
        case "right":
            data += "c0"

    # byte 14 = 16 (fixed)
    data += "100000"

    # byte 17 : check sum (256 remainders of the sum of 0~16 bytes)
    byte_sum = 0
    for i in range(0, len(data), 2):
        byte_sum += int(data[i : i + 2], 16)
    data += "{:02x}".format(byte_sum % 256)

    return data


def encode_aeha_to_bin(encoded_hex):
    bin_data = ""
    while len(encoded_hex) > 0:
        byte = "{:08b}".format(int(encoded_hex[:2], 16))
        bin_data += byte[::-1]
        encoded_hex = encoded_hex[2:]
    return bin_data


def encode_ir_signal(
    format: str,
    encoded_hex: str,
    unit_time: int,
    repeat: int,
):
    match format:
        case "AEHA":
            bin_data = encode_aeha_to_bin(encoded_hex)
            unit_frame = [unit_time * 8, unit_time * 4]
            for b in bin_data:
                if b == "0":
                    unit_frame.extend([unit_time, unit_time])
                else:
                    unit_frame.extend([unit_time, unit_time * 3])
            frame = []
            for i in range(repeat):
                frame += unit_frame
                frame += [unit_time, unit_time * 30]
            return frame


def main() -> None:
    # 引数をパース
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
       "on", "--power", type=str, required=True, help="power on/off"
    )
    arg_parser.add_argument("-m")
    arg_parser.add_argument_group()
    arg_parser.add_argument("id", nargs="+", type=str, help="IR codes")
    args = arg_parser.parse_args()
  
    with open(args.file, "r") as f:
       records = json.load(f)
    # print(encode_ir_signal("AEHA", encode_mitsubishi_aircon("on", "ac_move_eye", 26), 425, 2))


if __name__ == "__main__":
    main()
