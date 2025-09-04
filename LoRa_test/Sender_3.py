import serial
import sys
import time
import select

SERIAL_LORA = "/dev/ttyS0"
BAUDRATE = 115200

def main():
    ser_lora = serial.Serial(SERIAL_LORA, BAUDRATE, timeout=1)
    time.sleep(5)  # Arduino縺ｮ delay(5000) 逶ｸ蠖・
    print("LoRa bridge started. Type something and press Enter to send.")
    time.sleep(3)
    ser_lora.write("2".encode("ascii"))
    print("2")
    time.sleep(3)
    ser_lora.write("start".encode("ascii"))
    print("start")
    

    try:
        while True:
            # 繧ｿ繝ｼ繝溘リ繝ｫ蜈･蜉帙′縺ゅｌ縺ｰLoRa縺ｫ騾∽ｿ｡
            rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
            if rlist:
                line = sys.stdin.readline()
            try:
                # 入力を2進数文字列として解釈し、必要なバイト数に変換
                binary_data = int(line, 2).to_bytes((len(line) + 7) // 8, "big")
                print("Sending (binary):", binary_data)
                ser_lora.write(binary_data)

            except ValueError:
                print("value error (example: 10101100)")
                line = str(line).rstrip("\n") + "\r\n"
                print("Sending:",repr(line))
                ser_lora.write(line.encode("ascii"))

            # LoRa縺九ｉ蜿嶺ｿ｡縺後≠繧後・繧ｿ繝ｼ繝溘リ繝ｫ縺ｫ蜃ｺ蜉・           
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
