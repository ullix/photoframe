#!/usr/bin/python
"""Module docstring.

This serves as a long usage message.
"""
import Image
import ImageFont
import ImageDraw
import os
import sys
import ImageFilter
import ImageEnhance
import glob
import time
import usb.core
import usb.util
import pprint
import array
import StringIO
import sys
import getopt


import frame_utils

#print sys.argv
#print sys.byteorder
#print sys.builtin_module_names
#print sys.executable
#gs = glob.glob("/home/mm/bilder/timeline/*/*")
#for g in gs:
    #print g

#print len(gs)
#sys.exit()

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
          


print("\n\nBegin~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   
frame_utils.check_devices (known_devices_list)        

device = SPF87H_MiniMon
#device = SPF87H_MassSto

print("\nTrying to get device:",device[0])
dev = frame_utils.get_device(device)
if dev is not None:
    print("got it!")
    frame_utils.frame_init(dev)
else:
    print("Could not find it, exiting\n")
    sys.exit()



#fontpath =  "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
fontpath =  "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
sansfontbig     = ImageFont.truetype(fontpath, 160)
sansfontmedium  = ImageFont.truetype(fontpath, 100)
sansfontsmall   = ImageFont.truetype(fontpath,  25)


try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
except getopt.GetoptError, msg:
    print "msg is:",msg
    print "for help use --help"
    sys.exit(2)
# process options
for o, a in opts:
    if o in ("-h", "--help"):
        print __doc__
        sys.exit(0)
# process arguments
for arg in args:
    print "printing arg:",arg    
    #process(arg) # process() is defined elsewhere
    if arg == "init":
        wimage = Image.new("RGB",(800,480), "Chocolate")
        draw = ImageDraw.Draw(wimage)
        text = "Welcome"
        text_width, text_height = sansfontbig.getsize(text)
        #print "text_width, text_height",text_width, text_height
        draw.text((400 - text_width/2 , 240 - text_height/2 ), text, font=sansfontbig, fill="gold")
        output = StringIO.StringIO()
        wimage.save(output, "JPEG", quality=90)
        pic  = output.getvalue()
        output.close()
        l = len(pic)
        #print "len(pic) =", l, "chunks of 16384:",l/16384.,"q=",q
        frame_utils.jpg2frame(dev, pic)

        sys.exit()
        
print "finished with args..."



exepath = "/home/ullix/websites/local/photoframe/working"

path = "/home/mm/bilder/timeline/2009-11 Thanksgiving"
#path = "/home/mm/bilder/timeline/2009-10 San Diego"
path = "/home/mm/bilder/timeline/2011-07-21 Madeira"
path = "/home/mm/bilder/timeline/*"
#path = "/media/FC30-3DA9/DCIM/100MEDIA/"
#path = exepath


print ("\n--------------------------")


bilderlist = []
#bpath = path+'/SDC10402.JPG'
bilderlist  += glob.glob(path+'/*.JPG')
bilderlist  += glob.glob(path+'/*/*.JPG')

#bilderlist  += glob.glob(path+'/SDC1223[8-9]*.JPG')
#bilderlist  += glob.glob(path+'/SDC1223[8-9]*.JPG')
#bilderlist += glob.glob(path+"/*.jpg")
bilderlist += glob.glob(path+"/*/*.jpg")

#print "path:", path, "\nbpath:", bpath, "\nbilderlist:", bilderlist

bilderlist.sort(reverse=True)

#print bilderlist

print ("Laenge Bilderliste:",len(bilderlist))
time.sleep(0)

f = open('bigfile', 'w')

i=0 
counter = 0
errorcount = 0
ts =time.time()
for infile in bilderlist:
    i += 1
    #if i < 0 : continue
    #if i > 1000: break
    print( "\n__________________________")
    
    image = Image.open(infile)
    #image = Image.new("RGB",(800,480), "brown")
    
    print "\nimage as original is :",image.format, image.size, image.mode, infile
    #print( time.strftime("%d.%m.%Y %H:%M"))
 
    #print os.path.split(infile)
    #print os.path.dirname(infile)
    v = os.path.dirname(infile).rpartition('/')[2]
    
    
    if image.size != (800,480): 
        w = image.size[0]
        h = image.size[1]
        wh = float(w) / float(h)
        if wh < 1 : 
            print "Tall format, ignore"
            continue
        
        r = 800./480.
        #print("image w/h:", wh, "(frame 800/480=",r)
        if (wh > r * 1.05 or wh < r * 0.95): 
            w_crop = w 
            h_crop = w_crop / r 
            
            if h_crop <= h:
                h_delta_top = int((h - h_crop) / 4)
                h_delta_bottom = int((h - h_crop) * 3 / 4)                
                w_delta = int((w - w_crop) / 2)
                image = image.crop((0 + w_delta, 0 + h_delta_top, w - w_delta, h - h_delta_bottom)) 
        
            print "image after cropping: ", image.format, image.size, image.mode
        else:
            print("image was NOT cropped")    

        #image.show()
        image = image.resize((800,480))
        print "image after resizing: ",  image.format, image.size, image.mode

    else:
        print "image NOT resized and NOT cropped"
        
    #image.show()
    
    draw = ImageDraw.Draw(image)

    #draw.ellipse((350,100,450,400) , fill="purple", outline="white")
    draw.text((30, 20), "#"+str(i), font=sansfontmedium, fill="yellow")
    
    text = os.path.basename(infile)
    text_width, text_height = sansfontsmall.getsize(text)
    #print "text_width, text_height",text_width, text_height
    draw.text((800 - text_width - 2, text_height - 20 ), text, font=sansfontsmall, fill="red")
    draw.text((2, text_height - 20 ), v, font=sansfontsmall, fill="blue")

    draw.text((380, 305), time.strftime("%H:%M"), font=sansfontbig, fill="gold")

    q = 95   
    nl = "\n" # to make a NewLine when the first new quality needs to be recalculated
    limit = 23
    flag = False
    while True:
        output = StringIO.StringIO()
        image.save(output, "JPEG", quality=q)
        pic  = output.getvalue()
        output.close()
        l = len(pic)
        print "len(pic) =", l, "chunks of 16384:",l/16384.,"q=",q
        
        # in some 4000 photos, only 3 required a quality of 95 to stay under 23 chunks of 16384
        # none required 94 or less quality
        # 22 required 96
        # 124 required 97
        # ~700 required 98
        # so about 3000 could do with 99 
        # when the limit was 24, it failed with a  USBError('Operation timed out',) error after a few pictures!
        # conclusion: use limit of 23, and quality of 95, but still check for len of picture!
        if len(pic) < (16384 * limit) :
            if flag:
                f.write("OK " + "limit=" + str(limit) + " (" + str(16384 * limit) +"), " + infile + ", q=" + str(q) + ", l=" + str(l) + "\n")
            break
        else:
            flag = True
            f.write(nl + "   limit=" + str(limit) + " (" + str(16384 * limit) +"), " + infile + ", q=" + str(q) + ", l=" + str(l) + "\n")

        q -= 1
        nl = "" # reset new line
   
    #image.save("pyimage.jpg")
    #os.system(exepath+"/jpeg2spf87h -j pyimage.jpg")

    frame_utils.jpg2frame(dev, pic)


    #rcount = 1
    #tcs =time.time()
    #for ii in range(rcount):
    #    frame_utils.jpg2frame(dev, pic)
    #tce =time.time()    
    #print "for loop:",rcount,"loops", "Sec per pic: %.2f,  pic per sec: %.2f" %((tce - tcs)/rcount, rcount/(tce-tcs))
    
    counter +=1    
    te = time.time()
    print "Pictures written:",counter, ", Sec per pic: %.2f,  pic per sec: %.2f" %((te - ts)/counter, counter/(te-ts))
    time.sleep(2)

f.close 


print "Laenge Bilderliste:",len(bilderlist)