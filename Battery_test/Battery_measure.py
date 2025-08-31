import spidev
import time

# SPI初期化
spi = spidev.SpiDev()
spi.open(0, 0)   # SPI0, CE0 を使用
spi.max_speed_hz = 1000000  # 1MHz程度で十分

# ADCからデータを読む関数
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    # MCP3208は 3バイトやり取り
    # 送信: 1bitスタート + 1bitシングル/差動 + 3bitチャンネル + ダミー
    cmd = 0b11000 | channel      # 0b11 = start+single, D2D1D0=channel
    resp = spi.xfer2([cmd >> 2, (cmd & 0x03) << 6, 0])
    # 返ってくるデータは 12bit
    value = ((resp[1] & 0x0F) << 8) | resp[2]
    return value

# ADCの基準電圧(VREF)
VREF = 3.3   # 3.3Vを使っている場合

# 分圧比（例：R1=20kΩ, R2=10kΩ → 1/3）
DIV_RATIO = (20 + 10) / 10   # =3.0

try:
    while True:
        adc_val = read_adc(0)  # CH0を読む
        voltage = adc_val * VREF / 4096  # 分圧後の電圧
        lipo_voltage = voltage * DIV_RATIO  # 実際のリポ電圧に換算

        print(f"ADC Raw: {adc_val:4d}, Voltage: {voltage:.2f} V, LiPo: {lipo_voltage:.2f} V")
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
    print("終了しました")
