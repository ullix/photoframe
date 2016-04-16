/* $Id: usbreplay.c,v 1.7 2004/02/07 17:02:32 bd Exp $ */
/* Use only with the Hauppauge WinTV PVR usb2, VID/PID 2040/2900. */
/* No commercial affiliation, warranty, copyright, party invitation, */
/* fitness or non-fitness, implied or otherwise, is claimed by this comment. */
/* Compile with -lusb, then put it where capture.pl will find it. */

#include <usb.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>

struct usb_device *find_first_pvr() {
  struct usb_bus *bus;
  struct usb_device *dev;
  
  usb_init();
  usb_find_busses();
  usb_find_devices();
  
  for (bus = usb_busses; bus; bus = bus->next) {
    for (dev = bus->devices; dev; dev = dev->next) {
      if (dev->descriptor.idVendor == 0x04e8 &&
          dev->descriptor.idProduct == 0x2033) {
        fprintf(stderr, "Samsung photoframe in Mass Storage mode found ...\n");
        return dev;
      }
      else if (dev->descriptor.idVendor == 0x04e8 &&
               dev->descriptor.idProduct == 0x2034){
	fprintf(stderr, "Samsung photoframe in Custom Product mode found ...\n");
	return NULL;
      }
    }
  }
    fprintf(stderr, "No Samsung device found ...\n");
    return NULL;
}


int replay() {
  int res = -1;
  char buf[256];
  usb_dev_handle *udev;
  struct usb_device *dev = NULL;
  int numeps = 0;

  dev = find_first_pvr();
  if (dev == NULL) {
        fprintf(stderr, "Since no Samsung device in Mass Storage mode found, not going to do anything\n");
	return 0;
  }
  udev = usb_open(dev);

  setuid(getuid());

  strcpy(buf, "** no string **");
  res = usb_get_string_simple(udev, dev->descriptor.iManufacturer, buf, sizeof(buf));
  fprintf(stderr, "usb_get_string_simple => %d, %s\n", res, buf);

  char blah[254];
  memset(blah,0,254);

  res = usb_control_msg(udev, USB_TYPE_STANDARD | USB_ENDPOINT_IN, USB_REQ_GET_DESCRIPTOR, 0xfe, 0xfe, blah, 0xfe, 1000);
  printf("usb_control_msg() = %d\n",res);

  fprintf(stderr, "Just switched to 0x2028 now 2034! Custom Product mode\n");
  return 0;
}


int main(int argc, char *argv[]) {
  return replay();
}
