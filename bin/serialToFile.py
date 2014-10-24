#!/usr/bin/python
from Tkinter import *
import serial, threading
import _winreg as winreg

# ================ variable ==================
serialport_name = []

# ================ define ====================
# ================ threading =================
class serialInterface(threading.Thread):
    
    def __init__(self,port,baud):
        self.bufIndex = 0
        self.outdata = open('pdr_vs_cells@'+port+'.dat','w')
        self.inputBuf = ""
        self.lastByte = '\x7e'
        self.port = port
        self.baud = baud
        print "Receiving bytes from Seiral Port: " + str(port)
        self.serialPort_Handler = serial.Serial(port,baud)
        threading.Thread.__init__(self)
        
    def run(self):
        self.outdata.write("     ASN          SlotOffset          Frequency     \n")
        while True:
            try:
                rxBytes = self.serialPort_Handler.read(1)
            except:
                err = sys.exc_info()
                sys.stderr.write( "Error serialRx: %s (%s) \n" % (str(err[0]), str(err[1])))
            else:
                for rxByte in rxBytes:
                    if rxByte != '\x7e' and self.lastByte == '\x7e':
                        # start of frame
                        self.inputBuf           += '\x7e'
                        self.inputBuf           += rxByte
                    elif rxByte != '\x7e':
                        # middle of frame
                        self.inputBuf           += rxByte
                    elif rxByte == '\x7e':
                        # end of frame
                        self.inputBuf           += rxByte
                        self.expressData()
                        # self.outdata.write(self.inputBuf+'\n')
                        self.inputBuf = ""
                        
                    self.lastByte = rxByte
    
    def expressData(self):
        self.bufIndex += 1
        if len(self.inputBuf) < 3:
            self.bufIndex = 0
            return 
        if self.inputBuf[self.bufIndex] == 'D':
            pass
        elif self.inputBuf[self.bufIndex] == 'S':
            self.bufIndex += 1
            print "Thsi is a state frame: \n my address is : {0:x}-{1:x}".format(ord(self.inputBuf[self.bufIndex]),ord(self.inputBuf[self.bufIndex+1]))
            self.bufIndex += 2
            if ord(self.inputBuf[self.bufIndex]) == 0:
                self.bufIndex += 1
                self.parseIsSync()
            elif ord(self.inputBuf[self.bufIndex]) == 1:
                self.bufIndex += 1
                self.parseID()
            elif ord(self.inputBuf[self.bufIndex]) == 2:
                self.bufIndex += 1
                self.parseDAGRank()
            elif ord(self.inputBuf[self.bufIndex]) == 3:
                self.bufIndex += 1
                self.parseOutBufferIndexes()
            elif ord(self.inputBuf[self.bufIndex]) == 4:
                self.bufIndex += 1
                self.parseASN()
            elif ord(self.inputBuf[self.bufIndex]) == 5:
                self.bufIndex += 1
                self.parseMACStats()
            elif ord(self.inputBuf[self.bufIndex]) == 6:
                self.bufIndex += 1
                self.parseSchedule()
            elif ord(self.inputBuf[self.bufIndex]) == 7:
                self.bufIndex += 1
                self.parseBackOff()
            elif ord(self.inputBuf[self.bufIndex]) == 8:
                self.bufIndex += 1
                self.parseQueue()
            elif ord(self.inputBuf[self.bufIndex]) == 9:
                self.bufIndex += 1
                self.parseNeighbor()
            elif ord(self.inputBuf[self.bufIndex]) == 12:
                self.bufIndex += 1
                self.parseMyConcern()
            else:
                # print "Wrong state!"
                pass
            self.bufIndex = 0
        elif self.inputBuf[1] == 'I':
            pass
        elif self.inputBuf[1] == 'E':
            pass
        elif self.inputBuf[1] == 'C':
            pass
        elif self.inputBuf[1] == 'R':
            pass
            
        self.bufIndex = 0
            
    def parseIsSync(self):
        return
        
    def parseID(self):
        return
        
    def parseDAGRank(self):
        return
        
    def parseOutBufferIndexes(self):
        return
        
    def parseASN(self):
        return
        
    def parseMACStats(self):
        return 
        
    def parseSchedule(self):
        print "    Raw           : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    SlotOffset    : {0:d}".format(ord(self.inputBuf[self.bufIndex])+255*ord(self.inputBuf[self.bufIndex+1]))
        self.bufIndex += 2
        print "    type          : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    shared        : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    channelOffset : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    neighborAddr  : TODO"
        self.bufIndex += 17
        print "    numRx         : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    numTx         : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    numTxAck      : {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        print "    lastASN       : {0:d} {1:d} {2:d} {3:d} {4:d}".format(ord(self.inputBuf[self.bufIndex]),ord(self.inputBuf[self.bufIndex+1]),ord(self.inputBuf[self.bufIndex+2]),ord(self.inputBuf[self.bufIndex+3]),ord(self.inputBuf[self.bufIndex+4]))
        self.bufIndex += 5
        
    def parseBackOff(self):
        return 
        
    def parseQueue(self):
        return
        
    def parseNeighbor(self):
        return
    def parseMyConcern(self):
        input  = ""
        input += " {0:d} {1:d} {2:d} {3:d} {4:d}".format(ord(self.inputBuf[self.bufIndex]),ord(self.inputBuf[self.bufIndex+1]),ord(self.inputBuf[self.bufIndex+2]),ord(self.inputBuf[self.bufIndex+3]),ord(self.inputBuf[self.bufIndex+4]))
        self.bufIndex += 5
        input += "         {0:d}          ".format(ord(self.inputBuf[self.bufIndex])+255*ord(self.inputBuf[self.bufIndex+1]))
        self.bufIndex += 2
        input += "         {0:d}".format(ord(self.inputBuf[self.bufIndex]))
        self.bufIndex += 1
        self.outdata.write(input+'\n')
        
# ================== helper functions ===================
def findSerialPortName():
   global serialport_name
   path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
   key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
   for i in range(winreg.QueryInfoKey(key)[1]):
      try:
         val = winreg.EnumValue(key,i)
      except:
         pass
      else:
         if val[0].find('Silabser') > -1:
            serialport_name.append(str(val[1]))
# ========================= main ==========================
if __name__ == "__main__":
    findSerialPortName()
    for port in range(len(serialport_name)):
        temp = (serialInterface(serialport_name[port],115200))
        temp.start()