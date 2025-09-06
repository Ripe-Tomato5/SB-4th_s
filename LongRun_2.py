import spidev
import serial
import time
import csv
import os
from datetime import datetime
import smbus2

# ========================================
# LoRa UART 設定
# ========================================
SERIAL_LORA = "/dev/ttyS0"
BAUDRATE = 115200

# ========================================
# SPI 初期化 (ADC用 MCP3208など)
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

VREF = 5.0
DIV_RATIO = 1 / 2   # 分圧比

# ========================================
# BME280 I2C 設定
# ========================================
BME280_I2C_ADDR = 0x76
bus = smbus2.SMBus(1)

# 補正パラメータ取得
calib = bus.read_i2c_block_data(BME280_I2C_ADDR, 0x88, 24)
calib += bus.read_i2c_block_data(BME280_I2C_ADDR, 0xA1, 1)
calib += bus.read_i2c_block_data(BME280_I2C_ADDR, 0xE1, 7)

dig_T1 = calib[1] << 8 | calib[0]
dig_T2 = (calib[3] << 8 | calib[2]) - (1 << 16) if calib[3] & 0x80 else (calib[3] << 8 | calib[2])
dig_T3 = (calib[5] << 8 | calib[4]) - (1 << 16) if calib[5] & 0x80 else (calib[5] << 8 | calib[4])

dig_P1 = calib[7] << 8 | calib[6]
dig_P2 = (calib[9] << 8 | calib[8]) - (1 << 16) if calib[9] & 0x80 else (calib[9] << 8 | calib[8])
dig_P3 = (calib[11] << 8 | calib[10]) - (1 << 16) if calib[11] & 0x80 else (calib[11] << 8 | calib[10])
dig_P4 = (calib[13] << 8 | calib[12]) - (1 << 16) if calib[13] & 0x80 else (calib[13] << 8 | calib[12])
dig_P5 = (calib[15] << 8 | calib[14]) - (1 << 16) if calib[15] & 0x80 else (calib[15] << 8 | calib[14])
dig_P6 = (calib[17] << 8 | calib[16]) - (1 << 16) if calib[17] & 0x80 else (calib[17] << 8 | calib[16])
dig_P7 = (calib[19] << 8 | calib[18]) - (1 << 16) if calib[19] & 0x80 else (calib[19] << 8 | calib[18])
dig_P8 = (calib[21] << 8 | calib[20]) - (1 << 16) if calib[21] & 0x80 else (calib[21] << 8 | calib[20])
dig_P9 = (calib[23] << 8 | calib[22]) - (1 << 16) if calib[23] & 0x80 else (calib[23] << 8 | calib[22])

dig_H1 = calib[24]
dig_H2 = (calib[26] << 8 | calib[25]) - (1 << 16) if calib[26] & 0x80 else (calib[26] << 8 | calib[25])
dig_H3 = calib[27]
dig_H4 = (calib[28] << 4) | (calib[29] & 0x0F)
dig_H5 = (calib[30] << 4) | (calib[29] >> 4)
dig_H6 = calib[31] - 256 if calib[31] & 0x80 else calib[31]

# センサー初期化 (ctrl_hum, ctrl_meas, config)
bus.write_byte_data(BME280_I2C_ADDR, 0xF2, 0x01)  # humidity oversampling x1
bus.write_byte_data(BME280_I2C_ADDR, 0xF4, 0x27)  # temp/press oversampling x1, mode normal
bus.write_byte_data(BME280_I2C_ADDR, 0xF5, 0xA0)  # config

t_fine = 0

def read_bme280_all():
    global t_fine
    data = bus.read_i2c_block_data(BME280_I2C_ADDR, 0xF7, 8)

    # ADC 値取り出し
    adc_P = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    adc_T = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    adc_H = (data[6] << 8) | data[7]

    # 温度補正
    var1 = (((adc_T >> 3) - (dig_T1 << 1)) * dig_T2) >> 11
    var2 = (((((adc_T >> 4) - dig_T1) * ((adc_T >> 4) - dig_T1)) >> 12) * dig_T3) >> 14
    t_fine = var1 + var2
    temperature = float(((t_fine * 5 + 128) >> 8)) / 100.0

    # 気圧補正
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    if var1 == 0:
        pressure = 0
    else:
        p = 1048576.0 - adc_P
        p = (p - var2 / 4096.0) * 6250.0 / var1
        var1 = dig_P9 * p * p / 2147483648.0
        var2 = p * dig_P8 / 32768.0
        pressure = p + (var1 + var2 + dig_P7) / 16.0
        pressure /= 100.0  # hPa に変換

    # 湿度補正
    h = t_fine - 76800.0
    h = (adc_H - (dig_H4 * 64.0 + dig_H5 / 16384.0 * h)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * h * (1.0 + dig_H3 / 67108864.0 * h)))
    humidity = h * (1.0 - dig_H1 * h / 524288.0)
    if humidity > 100.0:
        humidity = 100.0
    elif humidity < 0.0:
        humidity = 0.0

    return temperature, pressure, humidity

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
    time.sleep(5)

    print("LoRa bridge + ADC + BME280(smbus2) started.")

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
                temperature, pressure, humidity = read_bme280_all()

                # 表示
                print(f"Elapsed: {elapsed_sec:4d} sec, "
                      f"LiPo: {lipo_voltage:.2f} V, "
                      f"Temp: {temperature:.2f} C, "
                      f"Hum: {humidity:.2f} %, "
                      f"Pres: {pressure:.2f} hPa")

                # CSV保存（強制書き込み）
                writer.writerow([
                    elapsed_sec,
                    f"{lipo_voltage:.2f}",
                    f"{temperature:.2f}",
                    f"{humidity:.2f}",
                    f"{pressure:.2f}"
                ])
                f.flush()
                os.fsync(f.fileno())

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
