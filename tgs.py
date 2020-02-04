import serial
import time

tgsCom    = "/dev/cu.usbmodem14201"  ##### MODIFY THIS LINE FOR YOUR SERIAL PORT NAME OR NUMBER
tgS = serial.Serial()
tgS.port = tgsCom
tgS.baudrate = 115200
tgS.bytesize = serial.EIGHTBITS #number of bits per bytes
tgS.parity = serial.PARITY_NONE #set parity check: no parity
tgS.stopbits = serial.STOPBITS_ONE #number of stop bits
#tgS.timeout = None          #block read
tgS.timeout = 0.5            #non-block read
tgS.xonxoff = False     #disable software flow control
tgS.rtscts = False     #disable hardware (RTS/CTS) flow control
tgS.dsrdtr = False       #disable hardware (DSR/DTR) flow control
tgS.writeTimeout = 0     #timeout for write


try: 
    print("Activating Triggerscope...")
    tgS.open()
except Exception as e:
    print ("ERROR: Triggerscope Com port NOT OPEN: " + str(e))
    exit()
if tgS.isOpen():
    try:
        tgS.flushInput() #flush input buffer, discarding all its contents
        tgS.flushOutput()#flush output buffer, aborting current output 
        tgS.write("*\n".encode() ) #send an ack to tgs to make sure it's up
        time.sleep(0.1)  #give the serial port sometime to receive the data
        print("Rx: " + tgS.readline().decode())
    except Exception as e1:
        print ("triggerscope serial communication error...: " + str(e1))

else:
    print ("cannot open triggerscope port ")

def writetgs(tgin):
    '''send a serial command to the triggerscope...
    Args:
        tgin: input string to send. Note the command terminator should be included in the string.
    Returns:
        char string of whatever comes back on the serial line. 
    Raises:
        none.
    '''
    scomp = '!'+tgin
    print(scomp)
    tgS.flushInput() #flush input buffer, discarding all its contents
    tgS.flushOutput()#flush output buffer, aborting current output 
    tgS.write(tgin.encode()) #send an ack to tgs to make sure it's up
    time.sleep(0.01)  #give the serial port sometime to receive the data 50ms works well...
    bufa = ""
    bufa = tgS.readline().decode()
    return bufa

def loadTgs():
    print ("Loading prog array..")
    for i in range(10):
        sout = ("PROG_TTL,%d,8,1\n" % (i+1) ) #prog command for triggerscope
        writetgs(sout)
        print (sout)
        time.sleep(0.01)
    print ("done.")

def armTgs():
    sout = ("ARM\n") #prog command for triggerscope
    writetgs(sout)
    print (sout)

def progtest():    
    print(writetgs("PROG_DAC,1,1,65000\n") )
    #print(writetgs("PROG_DAC,2,1,0\n") )

    print(writetgs("PROG_DAC,2,1,32000\n") )

    print(writetgs("PROG_TTL,1,1,1\n") )
    print(writetgs("PROG_TTL,2,2,1\n") )
    print(writetgs("ARM\n") )
    for n in range (10):
        print(tgS.readline())
        time.sleep(0.5)

#progtest()
print(writetgs("TTL1,1\n"))
dv = 32236
out = "DAC1,"+str(dv)+"\n"
print(out)




