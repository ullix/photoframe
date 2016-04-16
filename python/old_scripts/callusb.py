#!/usr/bin/python3

# For control transfer test
CTRL_LOOPBACK_WRITE = 0
CTRL_LOOPBACK_READ = 1

# to identify screens by USB Vendor and Product ID
# listed as: Name, idVendor, idProduct
#
# Samsung SPF87h in either mini monitor mode or mass storage mode
SPF87H_MiniMon  = ("SPF87H Mini Monitor", 0x04e8, 0x2034)
SPF87H_MassSto  = ("SPF87H Mass Storage", 0x04e8, 0x2033)
#          
# 4GB flash: 1e3d:2092
BFLASH4GB       = ("Flash Drive 4 GB", 0x1e3d, 0x2092)
         
known_devices_list  = [ SPF87H_MiniMon, SPF87H_MassSto, BFLASH4GB ]        
          
import usb.core
import usb.util
import sys
import pprint
import os
import struct
import array
import time

import callusb_utils

print("\n\nBegin~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#print('\x00' , 99)
#sys.exit()

#callusb_utils.show_user_info()

callusb_utils.check_devices (known_devices_list)        

device = SPF87H_MiniMon
#device = SPF87H_MassSto

print("\nTrying to get device:",device[0], end="       ")
dev = callusb_utils.get_device(device)
if dev is not None:
    print("got it!")
else:
    print("Could not find it, exiting\n")
    sys.exit()
   
print (">\n>")        
'''
print
for f1 in dev:
    print ("f1:", end="")
    pprint.pprint (f1, depth=9)
    for f2 in f1:
        print ("\tf2:", end="")
        pprint.pprint (f2, depth=9)
        for f3 in f2:
            print ("\t\tf3:",end="")
            pprint.pprint (f3, depth=9)
#            for f4 in f3:
#                print "\t\t\tf4:",
#                pprint.pprint (f4, depth=9)
#                for f5 in f4:
#                    print "\t\t\t\tf5:",
#                    pprint.pprint (f5)
'''           

'''
print ("\nbConfigurationValue\n\tbInterfaceNumber\n\t\tbEndpointAddress--------------")
for cfg in dev:
    print(str(cfg.bConfigurationValue) )
    for intf in cfg:
        print('\t' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) )
        for ep in intf:
            print('\t\t' + str(ep.bEndpointAddress) )
'''
    
# set the active configuration. With no arguments, the first
# configuration will be the active one
# Mini Monitor mode switches back off after transfer of pics
# not helpful to remain in pic mode
#dev.set_configuration()


#intf = cfg[0]

#cfg = dev.get_active_configuration()
#print ("Configuration Value:", cfg.bConfigurationValue)

#interface_number = cfg[(0,0)].bInterfaceNumber
#print ("interface number:", interface_number)

"""
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)
"""

# not helpful for keeping in Mini Monitor mode
#usb.util.release_interface(dev, 0)
#usb.util.claim_interface(dev, 0)


#ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
#            data_or_wLength = None, timeout = None):
    
#	unsigned char adata[0x0];
#   unsigned char bdata[0x00];

# !!! this seems to be required to keep the frame in Mini Monitor mode!!!
dev.ctrl_transfer(0xc0, 4, 0x0000, 0)       


path = '/home/ullix/websites/local/photoframe/working/'
filenames = ('red.jpg', 'image.jpg','blue.jpg', 'testimage.jpg', 'pyimage.jpg'  )

for fn in filenames:
    filename = path + fn
    
    infile = open(filename,"rb")
    #print("infile.tell", infile.tell())
    
    fstring = infile.read()
    #print("infile.tell", infile.tell())
    
    ls = len(fstring)
    print("\ninfile size by len:", ls, hex(ls) )
    
    #hdr1 = b"\xa5\x5a\x18\x04"
    #hdr3 = b"\x48\x00\x00\x00"
    #hdr2 = struct.pack('<I', ls)
    #hdr  = hdr1+hdr2+hdr3 
    hdr = b"\xa5\x5a\x18\x04" + struct.pack('<I', ls) + b"\x48\x00\x00\x00"
    
    data = hdr + fstring
    
    ##### total transfers must be completed 16x chunks ...
    # well maybe it needs a full 16384 complement = 2 ^14
    
    # find size of padding
    dl = len(data)
    pad = ((dl // 16384) +1) * 16384 - dl
    
    print("len of data is :", len(data), "len//16384=", len(data)//16384, "pad=", pad)
    
    #data += (16384 -14275 +16) * b'\x00'
    data += pad * b'\x00'    
    
    print ("Len von data after padding=", len(data))    
    
    
    #print("\ndata einzeln:")
    #for a in data[0:30]:
    #    print(hex(a), end=" ")
        
    
    #write(self, endpoint, data, interface = None, timeout = None):
    endpoint = 0x02
    #print("\nendpoint:", endpoint)
    
    i = 0
    sum = 0
    
    sum = dev.write(endpoint, data )
    while (0):
        start = i
        #ende  = i + (256*128)
        ende  = i + (16384)
        print (start, ende)
        d1 = data[ start : ende]  
        #print("d1:",d1)
        count = dev.write(endpoint, d1 )
        break
        print("no of bytes written:", count)
        sum += count
        i= ende 
        #if i > ls +12: break
        if i > 30000: break
    
    print("total bytes written:", sum)    
    
    #ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
    #            data_or_wLength = None, timeout = None):
    
    # this control is not needed!!!
    #rct = dev.ctrl_transfer(0xc0, 0x0006)
    #pprint.pprint(rct, depth=3)
    #print(rct[0:])
    #print(list(rct))

    time.sleep(0.311)

sys.exit()


assert ep is not None

# write the data
#ep.write(99)







#alternate_settting = usb.control.get_interface(interface_number)
#intf = usb.util.find_descriptor(
#    cfg, bInterfaceNumber = interface_number,
#    bAlternateSetting = alternate_setting
#)







sys.exit()
####################################################################################

print( 'BEFORE CHANGE:')
show_user_info()
print()

try:
       os.setegid(TEST_GID)
except OSError:
       print( 'ERROR: Could not change effective group.  Re-run as root.')
else:
       print( 'CHANGED GROUP:')
       show_user_info()
       print()

try:
       os.seteuid(TEST_UID)
except OSError:
       print( 'ERROR: Could not change effective user.  Re-run as root.')
else:
       print( 'CHANGE USER:')
       show_user_info()
       print()

TEST_GID=33
TEST_UID=33
