import spidev
import time
import csv
from datetime import datetime

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
VREF = 3.3

# 分圧比（例：R1=20kΩ, R2=10kΩ → 1/3）
DIV_RATIO = (20 + 10) / 10   # =3.0

# ログファイル名を日付付きにする
date_str = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"lipo_log_{date_str}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Elapsed Time (min)", "LiPo Voltage (V)"])

start_time = time.time()

try:
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        while True:
            adc_val = read_adc(0)
            voltage = adc_val * VREF / 4096
            lipo_voltage = voltage * DIV_RATIO
            elapsed_min = int((time.time() - start_time) / 60)

            # 表示
            print(f"Elapsed: {elapsed_min:4d} min, LiPo: {lipo_voltage:.2f} V")

            # CSV追記
            writer.writerow([elapsed_min, f"{lipo_voltage:.2f}"])

            time.sleep(60)

except KeyboardInterrupt:
    spi.close()
    print("終了しました")
