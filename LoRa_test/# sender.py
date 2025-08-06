# sender.py

import serial
import time

# UARTポート設定（115200bpsはES920LRの初期設定）
ser = serial.Serial(
    port='/dev/serial0',  # または '/dev/ttyS0'
    baudrate=115200,
    timeout=1
)

print("ES920LR 送信モード（Ctrl+Cで終了）")

try:
    while True:
        msg = input("[送信] 入力してください: ")
        if msg:
            # 改行付きで送信（CRLF推奨）
            ser.write((msg + '\r\n').encode('utf-8'))
            print("[送信完了]")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n送信を終了します。")

finally:
    ser.close()
