#ARC Example Python application for control and programming fo the triggerscope.
# note these examples are best used in conjunction with the triggerscope Syntax document, found at https://arc.austinblanco.com/product/triggerscope-4/

import serial
import time
import sys
import glob


#Searches for serial ports and provides a list to the user to choose from
if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')

result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)

    except (OSError, serial.SerialException):
        pass

print("\n")
print("Listing Available Serial Ports....\n")
x = 1
for n in result:
    print("Enter " + str(x) + " for " + n)
    x=x+1
print()
pNum = input("Select Com port # from list above to open.....:")

#open the port...
tgCom = result[int(pNum) - 1]
tgS = serial.Serial()
tgS.port = tgCom
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
        print(" serial communication error...: " + str(e1))

else:
    print("cannot open tg cell  port ")


#functions below each perform a sample experiment as documented in the command syntax documentation

#this command performs a write
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


#this uses the "STAT" command to report the current status of the triggerscope
def readStat():
    tgS.flushInput()  # flush input buffer, discarding all its contents
    tgS.flushOutput()  # flush output buffer, aborting current output
    tgS.write("STAT?\n".encode())  # send command
    time.sleep(0.02)  # give the serial port sometime to receive the data 50ms works well...
    for n in range(100):
        time.sleep(0.2)  # give the serial port sometime to receive the data 50ms works well...
        bufa = ""
        bufa = tgS.readline()
        print(bufa);
        if(len(bufa) < 5):
            break

def speedTestB():

    start = time.time()
    #input("Press Enter ...")
    speed = input("Enter speed in 16bit or esc to exit...")
    while speed != "esc":
        out = "PROG_WAVE,0,1,1,0,10000,"+str(speed)+",0,0,0\n"
        print("Sending:"+out)
        print(writetgs(out)) #waveArray [wave 1/2] , DAC, Form , center, amplitude, step per cycle, duty (if used), phase, trigger type ),
        print(writetgs("ARM\n"))
        speed = input("Enter speed in 16bit or esc to exit...")
        print(writetgs("\n"))
        clearSerial()




    #print(writetgs("*\n"))

    #print(writetgs("PROG_WAVE,0,1,1,15000,32000,1,0,0,0\n"))  # array zero, line 1, sine wave,center 5v, +/- 2.5V. one step per cycle, Duty cycle 0 (ignored for sine), no phase, freerun, no program step
    #print(writetgs("ARM\n"))
    #input("Press Enter ...")

    #print(writetgs("RANGE3,1\n"))
    #print(writetgs("RANGE4,1\n"))


def speedTestC():

    start = time.time()
    #input("Press Enter ...")
    speed = input("Enter speed in 16bit or esc to exit...")
    while speed != "esc":
        out = "PROG_WAVE,0,1,2,0,30000,"+str(speed)+",0,0,0\n"
        print("Sending:"+out)
        print(writetgs(out)) #waveArray [wave 1/2] , DAC, Form , center, amplitude, step per cycle, duty (if used), phase, trigger type ),
        print(writetgs("ARM\n"))
        speed = input("Enter speed in 16bit or esc to exit...")
        print(writetgs("\n"))
        clearSerial()

    #print(writetgs("*\n"))

    #print(writetgs("PROG_WAVE,0,1,1,15000,32000,1,0,0,0\n"))  # array zero, line 1, sine wave,center 5v, +/- 2.5V. one step per cycle, Duty cycle 0 (ignored for sine), no phase, freerun, no program step
    #print(writetgs("ARM\n"))
    #input("Press Enter ...")

    #print(writetgs("RANGE3,1\n"))
    #print(writetgs("RANGE4,1\n"))


def set10vdac():
    start = time.time()

    for i in range(17):
        print(writetgs("RANGE"+ str(i) + ",2\n"))

    #print(writetgs("RANGE1,1\n"))
    #print(writetgs("RANGE2,1\n"))
    #print(writetgs("RANGE3,1\n"))
    #print(writetgs("RANGE4,1\n"))
    print(writetgs("SAVESETTINGS\n"))

    for i in range(17):
        print(writetgs("DAC" + str(i) + ",65535\n"))

    input(" CHECK DAC HIGHS  @ 10V...")

    for i in range(17):
        print(writetgs("DAC" + str(i) + ",0\n"))
    input(" CHECK DAC LOWS")

    for i in range(13):
        print(writetgs("TTL" + str(i) + ",1\n"))
    input(" CHECK TTL 1-12 = 5V")

    for i in range(13):
        print(writetgs("TTL" + str(i) + ",0\n"))
    input("CHECK TTL 1-12 = 0.00V")

    input("Connect single lead from TTL 1 to TRIG 1. Press & to test cycling and reaction of TRIG LED")

    for i in range(30):
        writetgs("TTL" + str(i) + ",1\n")
        time.sleep(0.1)
        writetgs("TTL" + str(i) + ",0\n")
        time.sleep(0.1)

    print("Test Complete...")

def clearSerial():
    for n in range(100):
        print(writetgs("\n"))
        time.sleep(0.02)  # give the serial port sometime to receive the data 50ms works well...
        bufa = ""
        bufa = tgS.readline()
        print(bufa);
        if (len(bufa) < 5):
            break

def ttl1cyclesequence():
    print(writetgs("PROG_TTL,1,1,1\n"))
    print(writetgs("PROG_TTL,2,1,0\n"))
    print(writetgs("TIMECYCLES,5\n"))
    print(writetgs("ARM\n"))

def ttl1ttl2cyclesequence():
    print(writetgs("CLEAR_ALL\n"))
    print(writetgs("PROG_TTL,1,1,1\n"))
    print(writetgs("PROG_TTL,2,1,0\n"))
    print(writetgs("PROG_TTL,2,2,1\n"))
    print(writetgs("TIMECYCLES,5\n"))
    print(writetgs("ARM\n"))

def dac1stepsequence():
    print(writetgs("CLEAR_ALL\n"))
    print(writetgs("PROG_DAC,1,1,10000\n"))
    print(writetgs("PROG_DAC,2,1,20000\n"))
    print(writetgs("PROG_DAC,3,1,30000\n"))
    print(writetgs("TIMECYCLES,3\n"))
    print(writetgs("ARM\n"))

def focussequence():
    print(writetgs("CLEAR_ALL\n"))
    print(writetgs("PROG_FOCUS,1,10000,4,1,0\n")) #change last value to # 0 for channel first example!
    print(writetgs("PROG_TTL,1,1,1\n"))
    print(writetgs("PROG_TTL,2,2,1\n"))
    print(writetgs("PROG_TTL,2,1,0\n"))
    print(writetgs("TIMECYCLES,3\n"))
    print(writetgs("ARM\n"))


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

input("Press Enter ...")
#set10vdac()

#    UNCOMMENT EACH OF THESE TO TEST A GIVEN EXAPLE.
#ttl1cyclesequence()
#dac1stepsequence()
#ttl1ttl2cyclesequence()
focussequence()

