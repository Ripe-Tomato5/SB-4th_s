import serial
import time

# UARTポート設定
ser = serial.Serial(
    port='/dev/serial0',  # または '/dev/ttyS0'
    baudrate=115200,
    timeout=1
)

print("ES920LR バイナリ送信モード（Ctrl+Cで終了）")

try:
    while True:
        # ユーザー入力（16進で入力する想定）
        hex_str = input("[送信] 16進で入力してください (例: 01 02 FF): ").strip()

        if hex_str:
            try:
                # スペースやカンマ区切りでもOKにする
                hex_str = hex_str.replace(",", " ").replace("  ", " ")
                byte_data = bytes.fromhex(hex_str)  # 16進文字列 → バイト列
                ser.write(byte_data)
                print(f"[送信完了] {byte_data}")
            except ValueError:
                print("[エラー] 16進数として解釈できません。")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n送信を終了します。")

finally:
    ser.close()
