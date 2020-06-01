import serial
import time

tgsCom = "/dev/cu.usbmodem14101"
tgS = serial.Serial()
tgS.port = tgsCom
tgS.baudrate = 115200
tgS.bytesize = serial.EIGHTBITS  # number of bits per bytes
tgS.parity = serial.PARITY_NONE  # set parity check: no parity
tgS.stopbits = serial.STOPBITS_ONE  # number of stop bits
# tgS.timeout = None          #block read
tgS.timeout = 0.5  # non-block read
tgS.xonxoff = False  # disable software flow control
tgS.rtscts = False  # disable hardware (RTS/CTS) flow control
tgS.dsrdtr = False  # disable hardware (DSR/DTR) flow control
tgS.writeTimeout = 0  # timeout for write

try:
    print("Activating Triggerscope...")
    tgS.open()
except Exception as e:
    print("ERROR: Triggerscope Com port NOT OPEN: " + str(e))
    exit()
if tgS.isOpen():
    try:
        tgS.flushInput()  # flush input buffer, discarding all its contents
        tgS.flushOutput()  # flush output buffer, aborting current output
        op = "*"
        tgS.write(op.encode() + "\n".encode('ascii'))  # send an ack to tgs to make sure it's up
        time.sleep(0.2)  # give the serial port sometime to receive the data
        print("Rx: " + tgS.readline().decode())
    except Exception as e1:
        print("triggerscope serial communication error...: " + str(e1))

else:
    print("cannot open triggerscope port ")


def writetgs(tgin):
    '''send a serial command to the triggerscope...
    Args:
        tgin: input string to send. Note the command terminator should be included in the string.
    Returns:
        char string of whatever comes back on the serial line.
    Raises:
        none.
    '''
    tgS.flushInput()  # flush input buffer, discarding all its contents
    tgS.flushOutput()  # flush output buffer, aborting current output
    tgS.write(tgin.encode())  # send command
    time.sleep(0.02)  # give the serial port sometime to receive the data 50ms works well...
    bufa = ""
    bufa = tgS.readline()
    return bufa


def speedTestA():

   # for x in range (5):
   #     time.sleep(1)  # for the arduino reset
   #     print(x)
    start = time.time()

    print( writetgs("TIMECYCLES,3\n") )


    print( writetgs("PROG_TTL,1,1,1\n") )
    print( writetgs("PROG_TTL,1,2,0\n") )

    print( writetgs("PROG_TTL,2,1,0\n") )
    print( writetgs("PROG_TTL,2,2,1\n") )
    print( writetgs("PROG_TTL,2,3,0\n") )

    print( writetgs("PROG_TTL,3,1,0\n") )
    print( writetgs("PROG_TTL,3,2,0\n") )
    print( writetgs("PROG_TTL,3,3,1\n") )
    print( writetgs("PROG_TTL,3,4,0\n") )

    print( writetgs("ARM\n") )


def speedTestB():

   # for x in range (5):
   #     time.sleep(1)  # for the arduino reset
   #     print(x)
    start = time.time()

    print( writetgs("TIMECYCLES,3\n") )

    print( writetgs("PROG_FOCUS,32832,3276,4,1,0\n") )

    print( writetgs("PROG_TTL,1,1,1\n") )
    print( writetgs("PROG_TTL,1,2,0\n") )

    print( writetgs("PROG_TTL,2,1,0\n") )
    print( writetgs("PROG_TTL,2,2,1\n") )
    print( writetgs("PROG_TTL,2,3,0\n") )

    print( writetgs("PROG_TTL,3,1,0\n") )
    print( writetgs("PROG_TTL,3,2,0\n") )
    print( writetgs("PROG_TTL,3,3,1\n") )
    print( writetgs("PROG_TTL,3,4,0\n") )

    print( writetgs("ARM\n") )

def cyclettl():
    for i in range(30):
        print(writetgs("TTL1,1\n"))
        time.sleep(0.05)
        print(writetgs("TTL1,0\n"))
        time.sleep(0.05)

def cycledac():
    for i in range(30):
        print(writetgs("DAC1,"+str(2184*i)+"\n"))
        time.sleep(0.05)



input(" Check for TTL 1 on and off @ 10Hz - Arm Oscilloscope Press Enter ...")
cyclettl()

input(" Check for DAC 1 ramp @ 10Hz - Arm Oscilloscope Press Enter ...")
cycledac()


input(" Sweep over Channel First - Arm Oscilloscope Press Enter ...")
speedTestA()

input(" Sweep over Channel First - Arm Oscilloscope Press Enter ...")
speedTestB()
