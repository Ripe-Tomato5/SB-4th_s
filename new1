import serial
import sys
import time
import select

PC ↔ Raspberry Pi は標準的に /dev/ttyUSB0 や /dev/ttyAMA0 などを使う
LoRaモジュール側のシリアルポートは環境に応じて書き換えてください
例: USBシリアル変換なら /dev/ttyUSB0
GPIO UARTなら /dev/serial0
SERIAL_PC = "/dev/ttyUSB0"     # PCと接続している側
SERIAL_LORA = "/dev/serial0"   # LoRaモジュールに繋がっている側

BAUDRATE = 115200

def main():
    # シリアルポート初期化
    ser_pc = serial.Serial(SERIAL_PC, BAUDRATE, timeout=0)
    ser_lora = serial.Serial(SERIAL_LORA, BAUDRATE, timeout=0)

    time.sleep(5)  # Arduinoでdelay(5000)に相当

    print("Serial bridge started")

    try:
        while True:
            # PC → LoRa
            if ser_pc.in_waiting > 0:
                data = ser_pc.read(ser_pc.in_waiting)
                ser_lora.write(data)

            # LoRa → PC
            if ser_lora.in_waiting > 0:
                data = ser_lora.read(ser_lora.in_waiting)
                ser_pc.write(data)

            # CPUを占有しないように少し待つ
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        ser_pc.close()
        ser_lora.close()


if name == "main":
    main()
