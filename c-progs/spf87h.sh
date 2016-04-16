#!/bin/sh
killall conky 2>&1 >/dev/null
killall Xvfb 2>&1 >/dev/null
rm /tmp/.X13-lock 2>&1 >/dev/null
Xvfb :13 -screen 0 480x800x16 &
sleep 5
/home/sascha/SPF-87H/playusb/playusb -j /tmp/ram/xwud.jpg
export DISPLAY=:13.0
conky -p 0 -c /home/sascha/SPF-87H/conky/.conkyWeather &
conky -p 4 -c /home/sascha/SPF-87H/conky/.conkySystem &
conky -p 6 -c /home/sascha/SPF-87H/conky/.conkyCal &
conky -p 8 -c /home/sascha/SPF-87H/conky/nixie_clock.conkyrc &
while `grep -q 'Vendor=04e8 ProdID=2034' /proc/bus/usb/devices`
do
	scrot /tmp/ram/xwud.jpg -q 100
	jpegtran -rotate 90 -trim -outfile /tmp/ram/xwud.jpg /tmp/ram/xwud.jpg
	/home/sascha/SPF-87H/playusb/playusb -j /tmp/ram/xwud.jpg
done
killall conky 2>&1 >/dev/null
killall Xvfb 2>&1 >/dev/null
sudo rm /tmp/.X13-lock 2>&1 >/dev/null
exit 0