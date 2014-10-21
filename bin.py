# This file is part of stm32loader.
#
# stm32loader is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# stm32loader is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with stm32loader; see the file COPYING3.  If not see
# <http://www.gnu.org/licenses/>.

import sys, getopt

from bootloader import CommandInterface

try : 
    from serialport import SerialPorts
except OSError: 
    print "This is not Windows Environment!"

chip_ids = {
    0x412: "STM32 Low-density",
    0x410: "STM32 Medium-density",
    0x414: "STM32 High-density",
    0x420: "STM32 Medium-density value line",
    0x428: "STM32 High-density value line",
    0x430: "STM32 XL-density",
    0x416: "STM32 Medium-density ultralow power line",
    0x411: "STM32F2xx",
    0x413: "STM32F4xx",
}

def usage():
    print """Usage: %s [-hqVewvr] [-l length] [-p port] [-b baud] [-a addr] [-g addr] [file.bin]
    -h          This help
    -q          Quiet
    -e          Erase
    -w          Write
    -v          Verify
    -r          Read
    -l length   Length of read
    -p port     Serial port (default: COM6)
    -b baud     Baud speed (default:  115200)
    -a addr     Target address
    -g addr     Address to start running at (0x08000000, usually)
    -A          Write to all available port named 
                "\Device\VCPx", (Windows) or
                "\Device\Silabserx", (Windows) or
                "/dev/ttyUSBx", (Linux, TODO)
                one by one.
                It depends on the type of you USB to UART chip.

    example: 
    
    bin.py -p COM6 -e -w -v example/main.bin
    bin.py -A -q example/main.bin

    """ % sys.argv[0]

# define different type of devices. (Depending on the type of uart to usb chip)
VCP_DEVICES      = "\Device\VCP"
SILABSER_DEVICES = "\Device\Silabser"
LINUX_DEVICES    = "/dev/ttyUSBx"
    
# this function will download the target file to the device at 0x8000000 and verify.
def downloadJob(port):
    status = False # True instead of success, False instead of Failed
    print "Processing on " + port + "..."
    cmd = CommandInterface()
    
    if not conf['debuggingInfo']:
        cmd.quiet()
    
    conf['port'] = port
    
    cmd.open(conf['port'], conf['baud'])
    cmd.initChip()
    print "1. Erase memory first. Erasing..."
    cmd.cmdEraseMemory()
    print "2. Erase Done. Waiting for writing..."
    data = map(lambda c: ord(c), file(args[0], 'rb').read())
    cmd.writeMemory(conf['address'], data)
    print "3. EndOfWrite. Waiting for verifying..."
    verify = cmd.readMemory(conf['address'], len(data))
    if(data == verify):
        print "4. Verification OK"
        print "Download on port " + str(tmp[1]) + " successfully! :)"
        status = True
    else:
        print "4. Verification FAILED"
        print str(len(data)) + ' vs ' + str(len(verify))
        for i in xrange(0, len(data)):
            if data[i] != verify[i]:
                print hex(i) + ': ' + hex(data[i]) + ' vs ' + hex(verify[i])
    cmd.releaseChip()
    cmd.sp.close()
    return status

if __name__ == "__main__":

    conf = {
            'port'   : 'COM6',
            'baud'   : 115200,
            'address': 0x08000000,
            'erase'  : 0,
            'write'  : 0,
            'verify' : 0,
            'read'   : 0,
            'go_addr': -1,
            'all'    : 0,
            'debuggingInfo':1,
        }

# http://www.python.org/doc/2.5.2/lib/module-getopt.html

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hqVewvrp:b:a:l:g:A")
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-q':
            conf['debuggingInfo'] = 0
        elif o == '-h':
            usage()
            sys.exit(0)
        elif o == '-e':
            conf['erase'] = 1
        elif o == '-w':
            conf['write'] = 1
        elif o == '-v':
            conf['verify'] = 1
        elif o == '-r':
            conf['read'] = 1
        elif o == '-p':
            conf['port'] = a
        elif o == '-b':
            conf['baud'] = eval(a)
        elif o == '-a':
            conf['address'] = eval(a)
        elif o == '-g':
            conf['go_addr'] = eval(a)
        elif o == '-l':
            conf['len'] = eval(a)
        elif o == '-A':
            conf['all'] = 1
        else:
            assert False, "unhandled option"
    
# For "-A" options, downloading the target file on each connected VCP devices.
    if conf['all']:
        sPort = SerialPorts()
        sPort.enumerate_serial_ports()
        success = 0
        total = 0
        for x in range(len(sPort.portList)):
            tmp = sPort.portList[x]
            if tmp[0][:-1] == VCP_DEVICES or tmp[0][:-1] == SILABSER_DEVICES:
                total = total + 1
                print ""
                try:
                    status = downloadJob(str(tmp[1]))
                    if status:
                        success = success + 1
                except IOError:
                    print "Download on port " + str(tmp[1]) + " failed!  :("
        if x > 0:
            print "=================================================================="
            print "Job end: "+ str(100*float(success)/float(total)) + "% (" + str(success) + "/" + str(total) + ") devices are updated successfully!"
        else:
            print "No devices were found!"
        sys.exit(0)

# regular options: deal with one device
    cmd = CommandInterface()
    cmd.open(conf['port'], conf['baud'])
    
    if not conf['debuggingInfo']:
        cmd.quiet()
    
    cmd.mdebug( "Open port %(port)s, baud %(baud)d" % {'port':conf['port'], 'baud':conf['baud']})
    try:
        try:
            cmd.initChip()
        except IOError:
            print "Can't init. Ensure that BOOT0 is enabled and reset device"

        bootversion = cmd.cmdGet()
        cmd.mdebug("Bootloader version %X" % bootversion)
        id = cmd.cmdGetID()
        cmd.mdebug("Chip id: 0x%x (%s)" % (id, chip_ids.get(id, "Unknown")))

        if (conf['write'] or conf['verify']):
            data = map(lambda c: ord(c), file(args[0], 'rb').read())

        if conf['erase']:
            cmd.cmdEraseMemory()
            print "Erase Done."

        if conf['write']:
            cmd.writeMemory(conf['address'], data)

        if conf['verify']:
            verify = cmd.readMemory(conf['address'], len(data))
            if(data == verify):
                print "Verification OK"
            else:
                print "Verification FAILED"
                print str(len(data)) + ' vs ' + str(len(verify))
                for i in xrange(0, len(data)):
                    if data[i] != verify[i]:
                        print hex(i) + ': ' + hex(data[i]) + ' vs ' + hex(verify[i])

        if not conf['write'] and conf['read']:
            rdata = cmd.readMemory(conf['address'], conf['len'])
            file(args[0], 'wb').write(''.join(map(chr,rdata)))

        if conf['go_addr'] != -1:
            cmd.cmdGo(conf['go_addr'])

    finally:
        cmd.releaseChip()
        cmd.sp.close()


