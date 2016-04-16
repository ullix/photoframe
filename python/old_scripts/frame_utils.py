# some utilities for callusb
import os
import sys
import time
import usb.core
import usb.util
import struct

# show user and group ids
def show_user_info():
   print( 'Effective User  :', os.geteuid())
   print( 'Effective Group :', os.getegid())
   print( 'Actual User     :', os.getuid(), os.getlogin())
   print( 'Actual Group    :', os.getgid())
   print( 'Actual Groups   :', os.getgroups())
   return

# check for our known devices
def check_devices (devicelist):
    print("Check for presence of known devices:")
    for device in devicelist:
        if get_device(device) is not None :
            print("\tFound    :", device)
        else:
            print("\tNOT found:", device )
    print("..........")        
    return

def get_device(device):
    return usb.core.find(idVendor=device[1], idProduct=device[2])    



def jpg2frame(dev, pic):
    
    ts = time.time()
    ls = len(pic)
    hdr = b"\xa5\x5a\x18\x04" + struct.pack('<I', ls) + b"\x48\x00\x00\x00"
    rdata = hdr + pic
    
    ##### total transfers must be complete chunks of 16384  = 2 ^14. Complete by padding with zeros
    pad = 16384 - (len(rdata) % 16384) #+1 # +1 for test only
    data = rdata + pad * b'\x00'    

    #print "len of rdata is :", len(rdata), ", len/16384.=", len(rdata)/16384., ", pad=", pad, ", Len von data after padding=", len(data), "= 16384 *",len(data)/16384.

    endpoint = 0x02
    #print("\nendpoint:", endpoint)

    sum = 0
    errorflag = False
    #write(self, endpoint, data, interface = None, timeout = None):
    try:    
        sum = dev.write(endpoint, data , timeout=3000)
    except:
        errorflag = True
        print "\n!!!!!!!!!!!!!!!!!!!!! ERROR:", sys.exc_info()
        
    te = time.time() 
    print "total bytes written:", sum, "total chunks of 16384=", sum/16384.,  
    print "pic transfer only: Sec per pic: %.2f,  pic per sec: %.2f" %((te - ts), 1/(te-ts))
 
    if errorflag : 
        sys.exit()

    return

   
def frame_init(dev): 
    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    # Mini Monitor mode switches back off after transfer of pics
    # not helpful to remain in pic mode

    # not helpful for keeping in Mini Monitor mode
    #usb.util.release_interface(dev, 0)
    #usb.util.claim_interface(dev, 0)
    dev.set_configuration(1)
   
    #ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0, data_or_wLength = None, timeout = None):
    #	unsigned char adata[0x0];
    #   unsigned char bdata[0x00];
    # !!! this seems to be required to keep the frame in Mini Monitor mode!!!
    dev.ctrl_transfer(0xc0, 4, 0x0000, 0, timeout=2000)    
    return
    
  