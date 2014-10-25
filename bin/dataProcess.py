import threading
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import time

# ===================== define ======================
NUMOFCELLS = 9
NUMOFCHAN  = 16

TxFile = "pdr_vs_cells_COM22_-17dbm.dat"
RxFile = "pdr_vs_cells_COM5_-17dbm.dat"

slotPDR    = [[0 for m in range(NUMOFCHAN)] for i in range(NUMOFCELLS)]

# ==================== threading ====================
class processData(threading.Thread):
    def __init__(self,file):
        self.filename = file;
        self.file = open(file,'r')
        self.totalPkg = 0
        self.droppedPkg = 0;
        self.slotlist = [[0 for m in range(NUMOFCHAN)] for i in range(NUMOFCELLS)]
        threading.Thread.__init__(self)
        
    def run(self):
        for line in self.file:
            if line[0] == '#':
                continue
            self.totalPkg += 1
            try:
                dsn        = int(line[:10]) 
                asn        = int(line[11:20])
                slotoffset = int(line[21:30])
                assert slotoffset >=0 and slotoffset <NUMOFCELLS
                freq       = int(line[31:40])-11
                rssi       = int(line[41:50])
                lqi        = int(line[51:60])
                self.slotlist[slotoffset][freq] += 1
            except:
                self.droppedPkg += 1
                continue
                
        print "Dropped packages number: " + str(self.droppedPkg) + "\n"
        print "Totoal  packages number: " + str(self.totalPkg) + "\n"
 
# ==================== main ==========================
if __name__ == "__main__":
    processID1 = processData(TxFile)
    processID1.start()
    processID2 = processData(RxFile)
    processID2.start()
    
    time.sleep(2)
    
    # for i in range(NUMOFCELLS):
        # for j in range(NUMOFCHAN):
            # print "{0:^5}{1:^5}{2:^5}\n".format(i,j,processID1.slotlist[i][j])
    
    # plot
    x = np.int_([[ j for i in range(NUMOFCHAN)] for j in range(NUMOFCELLS)])
    y = np.int_([[ i for i in range(NUMOFCHAN)] for j in range(NUMOFCELLS)])
    z = np.int_(processID1.slotlist)
    
    fig = plt.figure()
    ax  = fig.gca(projection='3d')
    ax.plot_surface(x,y,z, rstride=8, cstride=8, alpha=0.3)
    # projection
    ax.contour(x, y, z, zdir='z', offset=0, cmap=cm.coolwarm)
    ax.contour(x, y, z, zdir='x', offset=0, cmap=cm.coolwarm)
    ax.contour(x, y, z, zdir='y', offset=16, cmap=cm.coolwarm)
    
    ax.set_xlabel('slotoffset')
    ax.set_xlim(0, 9)
    ax.set_ylabel('frequency')
    ax.set_ylim(0, 16)
    ax.set_zlabel('number of Tx packages')
    ax.set_zlim(0, 50)

    fig.show()
    
    # pdr vs channel
    channelTxCount = [0 for i in range(NUMOFCHAN)]
    channelRxCount = [0 for i in range(NUMOFCHAN)]
    channelPdrCount = [0.0 for i in range(NUMOFCHAN)]
    
    for i in range(NUMOFCELLS):
        for j in range(NUMOFCHAN):
            channelTxCount[j] += processID1.slotlist[i][j]
    
    for i in range(NUMOFCELLS):
        for j in range(NUMOFCHAN):
            channelRxCount[j] += processID2.slotlist[i][j]
   
    for i in range(NUMOFCHAN):
        channelPdrCount[i] = float(channelRxCount[i])/float(channelTxCount[i])
        
    x = np.int_([i for i in range(NUMOFCHAN)])
    y = np.float_(channelPdrCount)
    
    pdrCfig = plt.figure()
    ax = pdrCfig.gca()
    plt.bar(x, y, facecolor='blue')
    plt.grid(True)
    
    ax.set_xlabel('Channel')
    ax.set_xlim(0, 15)
    ax.set_xticks(x+0.5,[str(i) for i in range(NUMOFCHAN)])
    ax.set_ylabel('PDR')
    ax.set_ylim(0, 1)
    
    pdrCfig.show()
    
    # count vs channel
    y = np.float_(channelRxCount) 
    channelCountfig = plt.figure()
    ax = channelCountfig.gca()
    plt.bar(x, y, facecolor='green')
    plt.grid(True)
    
    ax.set_xlabel('Channel')
    ax.set_xlim(0, 15)
    ax.set_xticks(x+0.5,[str(i) for i in range(NUMOFCHAN)])
    ax.set_ylabel('Count')
    ax.set_ylim(0, 200)
    
    channelCountfig.show()
    
    
    
    # pdr vs slotoffset
    slotTxCount = [0 for i in range(NUMOFCELLS)]
    slotRxCount = [0 for i in range(NUMOFCELLS)]
    slotPdrCount = [0.0 for i in range(NUMOFCELLS)]
    
    for i in range(NUMOFCELLS):
        for j in range(NUMOFCHAN):
            slotTxCount[i] += processID1.slotlist[i][j]
    
    for i in range(NUMOFCELLS):
        for j in range(NUMOFCHAN):
            slotRxCount[i] += processID2.slotlist[i][j]
   
    for i in range(NUMOFCELLS):
        slotPdrCount[i] = float(slotRxCount[i])/float(slotTxCount[i])
        
    x = np.int_([i for i in range(NUMOFCELLS)])
    y = np.float_(slotPdrCount)
    
    pdrSfig = plt.figure()
    ax = pdrSfig.gca()
    plt.bar(x, y, facecolor='yellow')
    plt.grid(True)
    
    ax.set_xlabel('SlotOffset')
    ax.set_xlim(0, 9)
    ax.set_xticks(x+0.5,[str(i) for i in range(NUMOFCELLS)])
    ax.set_ylabel('PDR')
    ax.set_ylim(0, 1)
    
    pdrSfig.show()
    
    raw_input()