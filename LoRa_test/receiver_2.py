import serial
import time

# UARTポート設定
ser = serial.Serial(
    port='/dev/serial0',  # または '/dev/ttyS0'
    baudrate=115200,
    timeout=1
)

print("ES920LR バイナリ受信モード（Ctrl+Cで終了）")

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # 改行単位ではなく、受信可能なバイトをすべて取得
                data = ser.read(ser.in_waiting)  # バイト列(bytes型)

                if data:
                    # バイト列を16進表示
                    hex_str = data.hex(sep=" ").upper()
                    print(f"[受信] HEX: {hex_str} | RAW: {data}")
            except Exception as e:
                print(f"[受信エラー] {e}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n受信を終了します。")

finally:
    ser.close()
