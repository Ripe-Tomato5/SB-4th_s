import lora
import serial
import sys
import time

lr = lora.LoRa()

def sendcmd(cmd):
    print(cmd)
    lr.write(cmd)
    t = time.time()
    while (True):
        if (time.time() - t) > 5:
            print('panic: %s' % cmd)
            break
        line = lr.readline()
        if 'OK' in line:
            print(line)
            return True
        elif 'NG' in line:
            print(line)
            return False


def start():
    lr.reset()
    time.sleep(1.5)

    line = lr.readline()
    while not ('Mode' in line):
        lr.reset()
        line = lr.readline()
        if len(line) > 0:
            print(line)
        time.sleep(0.5)
    sendcmd('2\r\n')
    time.sleep(0.5)
    sendcmd('start\r\n')

def main():
    start()
    time.sleep(5)

    try:
        while True:

            if lr.in_waiting > 0:
                data = lr.read(lr.in_waiting)
                data = data.decode(errors="ignore")   
                sys.stdout.write(data.decode(errors="ignore"))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        lr.close()


if __name__ == "__main__":
    main()
