import serial
import time

class tgCom:
    def __init__(self, port=None):
        self.port = port
        self.ser = None
        self.waitTime = 0.05
        # Configure the serial port
        if self.port is None:
            self.port = input("Enter the serial port (e.g., COM3): ")

        try:
            self.ser = serial.Serial(self.port, 115200, timeout=1)
            print(f"Connected to {self.port} at {115200} baud.")
        except Exception as e:
            print(f"Error opening serial port: {e}")
            return

    def talk(self, command):
        # Send the command with a line feed
        self.ser.write((command + '\n').encode())
        print(f"Sent: {command}")

        # Wait for a response
        time.sleep(self.waitTime)  # Small delay to allow response
        response = self.ser.read_until(b'\n').decode().strip()
        if response:
            print(f"Received: {response}")
        else:
            print("No response received.")

    def close(self):
        self.ser.close()
        print(f"Closed connection to {self.port}.")


if __name__ == "__main__":
    #TODO  --- ( Notes on use)
    # Command Strucure as follows:
    # - Sending All "Zero" values to a given pin clears the use of that pin #
    # all configured pins will be executed, for now they are executed serially
    # --> meaning Wave 1 fires, then 2, then 3.
    # Command is
    #  n = DAC  # number(1 - 16)
    #  a = amplitude(0 - 32767) note that this is bipolar! so 16 bit/2 is max full output.
    #  o = offset(0 - 65535) 0 point offset adjust for full waveform
    #  u = updates - number of updates per sweep - or the time resolution of the waveform
    #  d = delay in microseconds between updates, will spread out waveform temporally
    tg = tgCom(port="/dev/cu.usbmodem173247101")  # Replace with your port
    print(tg.talk("PAS1-0-0"))
    print(tg.talk("PAS2-0-0"))

    print(tg.talk("BAO2-0-0"))  # turn blanking off for DAC2
    print(tg.talk("PAC1"))  # clear DAC2 sequence buffer (not strictly needed for WAV, but safe)

    print(tg.talk("PAC2"))  # clear DAC2 sequence buffer (not strictly needed for WAV, but safe)
    print(tg.talk("SAR1-4")) # set output voltage to +/- 10V
    print(tg.talk("SAR2-4"))

    print(tg.talk("WAV1-32767-32767-190-0")) # Example Waveform full span max rate
    print(tg.talk("WAV2-22767-32767-180-0"))
    print(tg.talk("PAS2-1-1"))
    print(tg.talk("PAS1-1-1"))

    #example that creates a full span waveform!
    if False:
        tg = tgCom(port="/dev/cu.usbmodem173247101")  # Replace with your port
        print(tg.talk("PAS1-0-0")) # begin watching for rising edge on TRIG 1, execute when detected.

        #print(tg.talk("SAR1-4")) # set output voltage to +/- 10V
        print(tg.talk("SAR2-4"))  # set output voltage to +/- 10V

        #print(tg.talk("WAV1-32767-32767-255-0")) # Example Waveform full span max rate
        print(tg.talk("WAV2-32767-32767-255-0"))  # Example Waveform full span max rate
        #print(tg.talk("PAS1-1-1")) # begin watching for rising edge on TRIG 1, execute when detected.
        print(tg.talk("PAS2-1-1"))  # begin watching for rising edge on TRIG 1, execute when detected.
    tg.close() # close COM port.

    # system will run until powered off or changed.
    if False:
        # example with half amplitude and altered offset!
        tg = tgCom(port="COM10")  # Replace with your port
        print(tg.talk("SAR1-4"))  # set output voltage to +/- 10V
        print(tg.talk("WAV1-16384-22767-100-2"))  # Example Waveform half span 2us delay (about 2x slower)
        print(tg.talk("PAS1-1-1"))  # begin watching for rising edge on TRIG 1, execute when detected.
        tg.close()  # close COM port.
