import serial
import time

# ===== UART設定 =====
SERIAL_PORT = "/dev/ttyS0"   # USB変換なら "/dev/ttyUSB0"
BAUDRATE = 115200

ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUDRATE,
    timeout=1
)

def send_payload(data: bytes):
    """
    入力データをバイナリフォーマットで送信
    data: 最大50バイト
    """
    length = len(data)
    if length > 50:
        raise ValueError("送信データは最大50バイトです")

    # フォーマット: [長さ(1byte)] + [データ本体]
    packet = bytes([length]) + data

    ser.write(packet)
    ser.flush()
    print("送信パケット:", packet)

def receive_response():
    data = ser.read(256)
    if not data:
        print("応答なし")
        return None
    
    try:
        # ASCII応答として解釈
        text = data.decode("ascii")
        print("受信(ASCII応答):", text.strip())
    except UnicodeDecodeError:
        # バイナリの場合
        print("受信(バイナリ):", data)
    
    return data


def main():
    try:
            # 応答を確認（必要なら）
            receive_response()

            time.sleep(0.2)  # 受信間隔

    except KeyboardInterrupt:
        print("終了します")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
