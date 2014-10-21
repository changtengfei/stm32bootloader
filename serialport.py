import _winreg as winreg
import itertools

class SerialPorts(object):
    # list contains all port device info
    portList = []

    def enumerate_serial_ports(self):
        """ Uses the Win32 registry to return a iterator of serial 
            (COM) ports existing on this computer.
        """
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except WindowsError:
            raise IterationError

        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                self.portList.append(val)
            except EnvironmentError:
                break

        winreg.CloseKey(key)

    def port_list(self):
        for x in range(len(self.portList)):
            tmp = self.portList[x]
            print tmp[0]
            print str(tmp[1])
