# some utilities for callusb
import os
import sys
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
         
    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    # Mini Monitor mode switches back off after transfer of pics
    # not helpful to remain in pic mode
    #dev.set_configuration()

    # not helpful for keeping in Mini Monitor mode
    #usb.util.release_interface(dev, 0)
    #usb.util.claim_interface(dev, 0)
    
    #ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
    #            data_or_wLength = None, timeout = None):
    #	unsigned char adata[0x0];
    #   unsigned char bdata[0x00];
    # !!! this seems to be required to keep the frame in Mini Monitor mode!!!
    dev.ctrl_transfer(0xc0, 4, 0x0000, 0)      
     
    fstring = pic     
    ls = len(fstring)
    print("\ninfile size by len:", ls, hex(ls) )
    
    hdr = b"\xa5\x5a\x18\x04" + struct.pack('<I', ls) + b"\x48\x00\x00\x00"
    
    data = hdr + fstring
    
    ##### total transfers must be completed 16x chunks ...
    # well maybe it needs a full 16384 complement = 2 ^14
    # find size of padding
    dl = len(data)
    pad = ((dl // 16384) +1) * 16384 - dl
    
    print("len of data is :", len(data), "len//16384=", len(data)//16384, "pad=", pad)

    data += pad * b'\x00'    
    
    print ("Len von data after padding=", len(data))    
    
    
    #print("\ndata einzeln:")
    #for a in data[0:30]:
    #    print(hex(a), end=" ")
    
    #write(self, endpoint, data, interface = None, timeout = None):
    endpoint = 0x02
    #print("\nendpoint:", endpoint)
    
    sum = dev.write(endpoint, data )
    print("total bytes written:", sum)    
    
    #ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
    #            data_or_wLength = None, timeout = None):
    
    # this control is not needed!!!
    #rct = dev.ctrl_transfer(0xc0, 0x0006)
    #pprint.pprint(rct, depth=3)
    #print(rct[0:])
    #print(list(rct))

    #time.sleep(0.311)
    return
    