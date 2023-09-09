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
    if power == "on":
        data += "20"
    elif power ==  "off":
        data += "00"
    else:
        raise (f"'{power}' is Invalid argument for 'power'.")

    # byte 6 : mode
    if mode == "ac_move_eye":
        data += "58"
    elif mode == "ac":
        data += "18"
    elif mode == "heat_move_eye":
        data += "48"
    elif mode == "heat":
        data += "08"
    elif mode == "dry_move_eye":
        data += "50"
    elif mode == "dry":
        data += "10"
    elif mode == "fan":
        data += "38"
    else:
        raise (f"'{mode}' is Invalid argument for 'mode'.")

    # byte 7 : temprature
    if 16 <= temp <= 31:
        data += "{:02x}".format(temp - 16)
    else:
        raise (f"'{temp}' is Invalid argument for 'temp'.")

    # byte 8 (upper 4bit) : wind direction (horizontal)
    if direction_h == "leftmost":
        data += "1"
    elif direction_h == "left":
        data += "2"
    elif direction_h == "center":
        data += "3"
    elif direction_h == "right":
        data += "4"
    elif direction_h == "rightmost":
        data += "5"
    elif direction_h == "swing":
        data += "c"
    else:
        raise (f"'{direction_h}' is Invalid argument for 'direction_h'.")

    # byte 8 (lower 4bit) : dry strength
    if mode == "ac" or mode ==  "ac_move_eye":
        data += "6"
    elif mode == "heat" or mode == "heat_move_eye" or mode == "fan":
        data += "0"
    elif mode == "dry" or mode ==  "dry_move_eye":
        if dry_strength == "high":
            data += "0"
        elif dry_strength == "middle":
            data += "2"
        elif dry_strength == "low":
            data += "4"

    # byte 9 (upper 2bit) : beep (once : 0b01, twice: 0b10)
    byte9_bin = "01"

    # byte 9 (middle 3bit) : wind direction (vertical)
    if direction_v == "auto":
        byte9_bin += "000"
    elif direction_v == "upmost":
        byte9_bin += "001"
    elif direction_v == "up":
        byte9_bin += "010"
    elif direction_v == "middle":
        byte9_bin += "011"
    elif direction_v == "down":
        byte9_bin += "100"
    elif direction_v == "downmost":
        byte9_bin += "101"
    elif direction_v == "swing":
        byte9_bin += "111"
    else:
        raise (f"'{direction_v}' is Invalid argument for 'direction_v'.")

    # byte 9 (lower 3bit) : wind strength
    if strength == "auto":
        byte9_bin += "000"
    elif strength == "low":
        byte9_bin += "001"
    elif strength == "middle":
        byte9_bin += "010"
    elif strength == "high":
        byte9_bin += "011"
    else:
        raise (f"'{strength}' is Invalid argument for 'strength'.")

    data += "{:02x}".format(int(byte9_bin, 2), "x")

    # byte 10 ~ 12 (fixed)
    data += "000000"

    # byte 13 : wind area
    if wind_area == "swing":
        data += "00"
    elif wind_area == "wide":
        data += "80"
    elif wind_area == "left":
        data += "40"
    elif wind_area == "right":
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
    if format == "AEHA":
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
