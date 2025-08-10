# receiver.py

import serial
import time

# UARTポート設定
ser = serial.Serial(
    port='/dev/serial0',  # または '/dev/ttyS0'
    baudrate=115200,
    timeout=1
)

print("ES920LR 受信モード（Ctrl+Cで終了）")

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # 改行単位で受信
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data:
                    print(f"[受信] {data}")
            except Exception as e:
                print(f"[受信エラー] {e}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n受信を終了します。")

finally:
    ser.close()
