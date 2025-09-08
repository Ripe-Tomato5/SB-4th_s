import serial
import sys
import time
import select

# LoRaモジュールのUARTデバイスを指定
# 例: USBシリアル変換なら /dev/ttyUSB0
#     GPIO UARTなら /dev/serial0
SERIAL_LORA = "/dev/serial0"
BAUDRATE = 115200

def main():
    ser_lora = serial.Serial(SERIAL_LORA, BAUDRATE, timeout=1)
    time.sleep(5)  # Arduinoの delay(5000) 相当

    print("LoRa bridge started. Type something and press Enter to send.")

    try:
        while True:
            # ターミナル入力があればLoRaに送信
            rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
            if rlist:
                line = sys.stdin.readline()
                ser_lora.write(line.encode("utf-8"))

            # LoRaから受信があればターミナルに出力
            if ser_lora.in_waiting > 0:
                data = ser_lora.read(ser_lora.in_waiting)
                sys.stdout.write(data.decode(errors="ignore"))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        ser_lora.close()


if __name__ == "__main__":
    main()