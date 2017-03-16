import platform
import argparse
import time
import serial

operating_system = platform.system()
port = None

if operating_system == 'Linux':
    port = '/dev/ttyACM0'
elif operating_system == 'Windows':
    port = 'COM3'

parser = argparse.ArgumentParser(description="StackPic utility :)")
parser.add_argument('--delay', '-d', dest='delay', required=False, help="Delay between steps "
                                                                                   "(have priority over Step per Sec")
parser.add_argument('--signal', '-s', dest='signal', required=False, default='+', help="Signal to send [+/-]")
parser.add_argument('--step_per_sec', '-sps', dest='step_per_sec', required=False, help="Step per second")
parser.add_argument('--port', '-p', dest='port', required=False, default=port, help="Port to send data")
parser.add_argument('--baud', '-b', dest='baud', required=False, default=9600, help="Baud rate of the "
                                                                                    "serial connection")
parser.add_argument('--simulation', '-sim', dest='simulation', required=False, action='store_true', default=False,
                    help="Emulate the serial port")
args = parser.parse_args()

if args.delay is not None:
    delay = float(args.delay)
else:
    delay = None

if args.step_per_sec is not None:
    step_per_sec = float(args.step_per_sec)
else:
    step_per_sec = None

baud = int(args.baud)
signal = args.signal.encode()
port = args.port

ser = None

if not args.simulation:
    ser = serial.Serial(port, baud)

if delay is not None:
    pass
elif delay is None and step_per_sec is not None:
    delay = 1.0 / step_per_sec
else:
    print("Incomplete argument, must be able to determine delay between step from arguments")
    exit()

try:
    while True:
        print("Sending: {}".format(signal))
        if ser is not None:
            ser.write(signal)
        time.sleep(delay)
except serial.portNotOpenError:
    print("Error port closed... Did ya unplug tha arduino?")
except serial.writeTimeoutError:
    print("Timeout error... Time's OUT")
except KeyboardInterrupt:
    print("Ok ok, I stop")
finally:
    if ser is not None:
        ser.close()
