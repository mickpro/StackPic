import platform
import argparse
import time
import serial
from math import floor

operating_system = platform.system()
port = None

if operating_system == 'Linux':
    port = '/dev/ttyACM0'
elif operating_system == 'Windows':
    port = 'COM5'

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
parser.add_argument('--step_per_delay', '-spd', dest='step_per_delay', required=False, default=1, help='Number of step per delay')
parser.add_argument('--deep_of_field', '-dof', dest='dof', required=False, help='Deep of field of the camera (cm)')

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
signal = args.signal
port = args.port
step_per_delay = int(args.step_per_delay)

if args.dof is not None:
    dof = float(args.dof)
    step_per_delay = (floor(dof / 0.00012/5))

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
        start_time = time.time()
        print("Sending: {} {} times".format(signal, step_per_delay))
        if ser is not None:
            for i in range(step_per_delay):
                ser.write(signal.encode())
        end_time = time.time()
        delta_time = end_time - start_time
        delay_time = delay - delta_time
        if delay_time < 0:
            raise ValueError
        time.sleep(delay_time)
except serial.portNotOpenError:
    print("Error port closed... Did ya unplug tha arduino?")
except serial.writeTimeoutError:
    print("Timeout error... Time's OUT")
except KeyboardInterrupt:
    print("Ok ok, I stop")
except ValueError:
	print("Delay too small for step per delay")
finally:
    if ser is not None:
        ser.close()