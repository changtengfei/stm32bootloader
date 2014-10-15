This repository is a re-distribution of Ivan's project (Project page: http://tuxotronic.org/wiki/projects/stm32loader)

Hardware setup
===========
In the original version, using this script need to corporate with the set and reset on BOOT0 and RESET pin. The set and reset usually were executed by hand. To create a totally automatic download process, you need to modified your hardware stm32 devices. Following are the steps you need to follow:

1. Identify you UART-to-USB Chip you are using and find the RTS and DTR pin. 
2. Connect the RTS pin on your UART-to-USB Chip to the BOOT0 pin on you STM32 device
3. Connect the DTR pin on your UART-to-USB Chip to the RESET pin on you STM32 device  

Note: For the connection of pins in steps 2 and 3, you can change the order in an opposite way(RTS->RESET, DTR->BOOT0). If you do this, you need exchange the usage of setRTS() and setDTR() functions in bootloader.py. 

STM32Loader
===========

Python script which will talk to the STM32 bootloader to upload and download firmware.

Usage: ./bin.py [-hqVewvr] [-l length] [-p port] [-b baud] [-a addr] [file.bin]
    -h          This help
    -q          Quiet
    -e          Erase
    -w          Write
    -v          Verify
    -r          Read
    -l length   Length of read
    -p port     Serial port (default: /dev/tty.usbserial-ftCYPMYJ)
    -b baud     Baud speed (default: 115200)
    -a addr     Target address
    -A          Write to all available port named 
                "\Device\VCPx", (Windows) or
                "\Device\Silabserx", (Windows) or
                "/dev/ttyUSBx", (Linux, TODO)
                one by one.
                It depends on the type of you USB to UART chip.

    ./bin.py -e -w -v example/main.bin


Example:
bin.py -e -w -v somefile.bin

This will pre-erase flash, write somefile.bin to the flash on the device, and then perform a verification after writing is finished.

bin.py -A somefile.bin

This will scan the SERIALCOM key in registered and write somefile.bin through each port named by "\Device\VCPx" and "\Device\Silabserx" one by one.

