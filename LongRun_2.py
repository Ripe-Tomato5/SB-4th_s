import spidev
import serial
import time
import csv
import os
from datetime import datetime
import smbus2
from adafruit_bme280 import basic as adafruit_bme280
import board

# ========================================
# LoRa UART 設定
# ========================================
SERIAL_LORA = "/dev/ttyS0"
BAUDRATE = 115200

# ========================================
# SPI 初期化 (ADC用)
# ========================================
spi = spidev.SpiDev()
spi.open(0, 0)   # SPI0, CE0
spi.max_speed_hz = 1000000

def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    cmd = 0b11000 | channel
    resp = spi.xfer2([cmd >> 2, (cmd & 0x03) << 6, 0])
    value = ((resp[1] & 0x0F) << 8) | resp[2]
    return value

VREF = 5
DIV_RATIO = 1 / 2

# ========================================
# BME280 設定
# ========================================
BME280_I2C_ADDR = 0x76
i2c = board.I2C()  
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=BME280_I2C_ADDR)

# ========================================
# CSV ファイル設定
# ========================================
date_str = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"lipo_bme280_log_{date_str}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Elapsed Time (sec)",
        "LiPo Voltage (V)",
        "Temperature (C)",
        "Humidity (%)",
        "Pressure (hPa)"
    ])

start_time = time.time()

# ========================================
# メイン処理
# ========================================
def main():
    ser_lora = serial.Serial(SERIAL_LORA, BAUDRATE, timeout=1)
    time.sleep(5)  # LoRa起動待ち

    print("LoRa bridge + ADC + BME280 started.")

    try:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)

            while True:
                # LoRa送信
                line = "1\n"
                ser_lora.write(line.encode("utf-8"))
                print(f"Sent: {line.strip()}")

                # LiPo電圧測定
                adc_val = read_adc(0)
                voltage = adc_val * VREF / 4096
                lipo_voltage = voltage * DIV_RATIO
                elapsed_sec = int(time.time() - start_time)

                # BME280 測定
                temperature = bme280.temperature
                humidity = bme280.humidity
                pressure = bme280.pressure

                # 表示
                print(f"Elapsed: {elapsed_sec:4d} sec, "
                      f"LiPo: {lipo_voltage:.2f} V, "
                      f"Temp: {temperature:.2f} C, "
                      f"Hum: {humidity:.2f} %, "
                      f"Pres: {pressure:.2f} hPa")

                # CSV保存（都度flush & fsync）
                writer.writerow([
                    elapsed_sec,
                    f"{lipo_voltage:.2f}",
                    f"{temperature:.2f}",
                    f"{humidity:.2f}",
                    f"{pressure:.2f}"
                ])
                f.flush()
                os.fsync(f.fileno())  # SDカードに強制書き込み

                time.sleep(30)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        ser_lora.close()
        spi.close()
        print("終了しました")

# ========================================
# 実行
# ========================================
if __name__ == "__main__":
    main()
