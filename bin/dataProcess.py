import threading
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# ===================== define ======================
NUMOFCELLS = 10
NUMOFCHAN  = 16

TxFile = "pdr_vs_cells@COM21.dat"
RxFile = "pdr_vs_cells@COM5.dat"

slotlistTx = [[0 for m in range(NUMOFCHAN)] for i in range(NUMOFCELLS)]
slotlistRx = [[0 for m in range(NUMOFCHAN)] for i in range(NUMOFCELLS)]
slotPDR    = [[0 for m in range(NUMOFCHAN)] for i in range(NUMOFCELLS)]

# ==================== threading ====================
class processData(threading.Thread):
    def __init__(self,file):
        self.filename = file;
        self.file = open(file,'r')
        self.droppedPgk = 0;
        threading.Thread.__init__(self)
        
    def run(self):
        for line in self.file:
            if line[0] == '#':
                continue
            try:
                dsn        = int(line[:10]) 
                asn        = int(line[11:20])
                slotoffset = int(line[21:30])
                freq       = int(line[31:40])-11
                rssi       = int(line[41:50])
                lqi        = int(line[51:60])
                slotlistTx[slotoffset][freq] += 1
            except:
                self.droppedPgk += 1
                continue
                
        print "Dropped packets number: " + str(self.droppedPgk) + "\n"
            

# ==================== main ==========================
if __name__ == "__main__":
    processID1 = processData(TxFile)
    processID1.start()
    processID2 = processData(RxFile)
    processID2.start()
    # plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = np.int_([[ j for i in range(NUMOFCHAN)] for j in range(NUMOFCELLS)])
    y = np.int_([[ i for i in range(NUMOFCHAN)] for j in range(NUMOFCELLS)])
    z = np.int_(slotlistTx)
    ax.plot_surface(x,y,z, rstride=8, cstride=8, alpha=0.3)

    ax.set_xlabel('X')
    ax.set_xlim(0, 10)
    ax.set_ylabel('Y')
    ax.set_ylim(0, 16)
    ax.set_zlabel('Z')
    ax.set_zlim(0, 20)

    plt.show()
   
    