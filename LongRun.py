import spidev
import serial
import time
import csv
from datetime import datetime


# LoRaモジュールのUARTデバイスを指定
# 例: USBシリアル変換なら /dev/ttyUSB0
#     GPIO UARTなら /dev/serial0
SERIAL_LORA = "/dev/serial0"
BAUDRATE = 115200

# SPI初期化
spi = spidev.SpiDev()
spi.open(0, 0)   # SPI0, CE0 を使用
spi.max_speed_hz = 1000000  # 1MHz程度で十分

# ADCからデータを読む関数
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    cmd = 0b11000 | channel
    resp = spi.xfer2([cmd >> 2, (cmd & 0x03) << 6, 0])
    value = ((resp[1] & 0x0F) << 8) | resp[2]
    return value

# ADCの基準電圧(VREF)
VREF = 5

# 分圧比（例：R1=20kΩ, R2=10kΩ → 1/3）
DIV_RATIO = 7.7 / 5.1   # =1.5098...

# ログファイル名を日付付きにする
date_str = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"lipo_log_{date_str}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Elapsed Time (sec)", "LiPo Voltage (V)"])

start_time = time.time()

def main():
    ser_lora = serial.Serial(SERIAL_LORA, BAUDRATE, timeout=1)
    time.sleep(5)  # Arduinoの delay(5000) 相当

    print("LoRa bridge started. Type something and press Enter to send.")

    try:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            
            while True:
                # LoRaに送信処理1と改行を30秒おきに送信
                line = "1\n"
                ser_lora.write(line.encode("utf-8"))
                print(f"Sent: {line.strip()}")

                adc_val = read_adc(0)
                voltage = adc_val * VREF / 4096
                lipo_voltage = voltage * DIV_RATIO
                elapsed_sec = int(time.time() - start_time)

                # 表示
                print(f"Elapsed: {elapsed_sec:4d} sec, LiPo: {lipo_voltage:.2f} V")

                # CSV追記
                writer.writerow([elapsed_sec, f"{lipo_voltage:.2f}"])

                time.sleep(30)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        ser_lora.close()
        spi.close()
        print("終了しました")


if __name__ == "__main__":
    main()