#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import usb.core
import usb.util
import StringIO
import Image
import struct

def write_jpg2frame(dev, pic):
    """Attach header to picture, pad with zeros if necessary, and send to frame"""
    # create header and stack before picture
    # middle 4 bytes have size of picture 
    rawdata = b"\xa5\x5a\x18\x04" + struct.pack('<I', len(pic)) + b"\x48\x00\x00\x00" + pic 
    # total transfers must be complete chunks of 16384  = 2 ^14. Complete by padding with zeros
    pad = 16384 - (len(rawdata) % 16384) +1          
    tdata = rawdata + pad * b'\x00'
    ltdata = len(tdata) 
    # Syntax: write(self, endpoint, data, interface = None, timeout = None):
    endpoint = 0x02                
    dev.write(endpoint, tdata )
    

def get_known_devices():
    """Return a dict of photo frames"""
    # listed as: Name, idVendor, idProduct, [width , height - in pixel if applicable] 
    #
    # Samsung SPF-87H in either mini monitor mode or mass storage mode
    SPF87H_MiniMon   = {'name':"SPF87H Mini Monitor", 'idVendor':0x04e8, 'idProduct':0x2034, 'width':800, 'height':480 }
    SPF87H_MassSto   = {'name':"SPF87H Mass Storage", 'idVendor':0x04e8, 'idProduct':0x2033}
    
    # Samsung SPF-107H (data from web reports - not tested)
    SPF107H_MiniMon  = {'name':"SPF107H Mini Monitor", 'idVendor':0x04e8, 'idProduct':0x2036, 'width':1024, 'height':600 }
    SPF107H_MassSto  = {'name':"SPF107H Mass Storage", 'idVendor':0x04e8, 'idProduct':0x2035}
    
    # Samsung SPF-83H (data from web reports - not tested)
    SPF107H_MiniMon  = {'name':"SPF107H Mini Monitor", 'idVendor':0x04e8, 'idProduct':0x200d, 'width':800, 'height':600 }
    SPF107H_MassSto  = {'name':"SPF107H Mass Storage", 'idVendor':0x04e8, 'idProduct':0x200c}
    
    return    ( SPF87H_MiniMon, SPF87H_MassSto, SPF107H_MiniMon, SPF107H_MassSto, SPF107H_MiniMon, SPF107H_MassSto )
 

def find_device(device):
    """Try to find device on USB bus."""
    return usb.core.find(idVendor=device['idVendor'], idProduct=device['idProduct'])    


def init_device(device0, device1):
    """First try Mini Monitor mode, then Mass storage mode"""
    dev = find_device(device0)
 
    if dev is not None:
        ## found it, trying to init it
        frame_init(dev)
    else:
        # not found device in Mini Monitor mode, trying to find it in Mass Storage mode
        dev = find_device(device1)
        if dev is not None:
            #found it in Mass Storage, trying to switch to Mini Monitor 
            frame_switch(dev)
            ts = time.time()
            while True:
                # may need to burn some time
                dev = find_device(device0)
                if dev is not None:
                    #switching successful
                    break
                elif time.time() - ts > 2:
                    print "switching failed. Ending program"
                    sys.exit()
            frame_init(dev)
        else:
            print "Could not find frame in either mode"
            sys.exit()
    return dev

   
def frame_init(dev): 
    """Init device so it stays in Mini Monitor mode"""
    # this is the minimum required to keep the frame in Mini Monitor mode!!!
    dev.ctrl_transfer(0xc0, 4 )    
  

def frame_switch(dev):
    """Switch device from Mass Storage to Mini Monitor"""  
    dev.ctrl_transfer(0x00|0x80,  0x06, 0xfe, 0xfe, 0xfe )
    # settling of the bus and frame takes about 0.42 sec
    # give it some extra time, but then still make sure it has settled
    time.sleep(1)

    
def main():
    global dev, known_devices_list
    
    known_devices_list = get_known_devices()

    # define which frame to use, here use Samsung SPF-87H 
    device0 = known_devices_list[0] # Mini Monitor mode
    device1 = known_devices_list[1] # Mass Storage mode

    dev = init_device(device0, device1)    
    print "Frame is in Mini Monitor mode and initialized. Sending pictures now" 

    image = Image.open("mypicture.jpg")
    #manipulations to consider:
    #  convert
    #  thumbnail
    #  rotate
    #  crop
    image = image.resize((800,480))
    output = StringIO.StringIO()
    image.save(output, "JPEG", quality=94)
    pic  = output.getvalue()
    output.close()
    write_jpg2frame(dev, pic)        
       

if __name__ == "__main__": 
    main()
