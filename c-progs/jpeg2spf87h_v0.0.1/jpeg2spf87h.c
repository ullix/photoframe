/* $Id: jpeg2spf87h,v 0.0.1 2011/01/28 22:41:54

   Use with the Samsung SPF-87H.
   Desgined and written for Firmware M-IR8HSBWW-1007.0 which is broken
   by design but should work with other, too.
   Compile with make.

   This software acts as a command and has options.
   It is used to send jpeg pictures to the device with no test about the
   jpeg file if the device is in monitor mode. Use spf87hd or similar to
   enable that if needed.
   I use jpeg2spf87h testpic.jpg.
   Try jpeg2spf87h --help.
   You need to have the jpeg file in dimensions and color depth the device
   can display. For the Samsung SPF-87H it is 800x430 pixel at landscape
   orientation, I use 16 bit color depth.

   jpeg2spf87h was inspired by playusb available 
   at http://vdrportal.de/board/thread.php?postid=951818#post951818

   No commercial affiliation, warranty, copyright, party invitation,
   fitness or non-fitness, implied or otherwise, is claimed by this comment.
   Compile with make. 

   This software is free of charge. It has no warranty, copyright, fitness or
   non-fitness, implied or otherwise, use it at own risk. It is deciated to
   the GPL License.

   You can find it at http://www.killerhippy.de

   Sascha Wüstemann
   2011-01-28 v.0.0.1 - Initial Version
   
   Thanks to Grace Woo:
   http://web.media.mit.edu/~gracewoo/stuff/picframe/
   Vadim Zaliva:
   http://notbrainsurgery.livejournal.com/38622.html
   and "andi" Andre Puschmann:
   http://vdrportal.de/board/thread.php?postid=951818#post951818

*/

#include <stdlib.h> // exit, abort
#include <getopt.h> // long options
#include <libusb-1.0/libusb.h> // device handling
#include <stdio.h> // fprintf
#include <unistd.h> // sleep
#include <string.h> // memcpy

#define VENDOR_ID 0x04e8 // Samsung SPF-87H
#define PRODUCT_ID 0x2034 // Monitor Mode
#define URBBUF_MAX 0x20000
#define USB_HDR_LEN 12
#define MAX_JPEG_SIZE (2 * 1024 * 1024)

void show_help(char* prg)
{
 printf("%s [OPTIONS]\n", prg);
 printf("\t-h, --help\tthis help\n"\
        "\t-j, --jpgfilename\tJPEG file\n\n");
}

int send_jpeg(FILE *file)
{
 char usb_hdr[USB_HDR_LEN] = {0xa5, 0x5a, 0x18, 0x04, 0xff, 0xff, 0xff, 0xff, 0x48, 0x00, 0x00, 0x00};
 unsigned char buffer[URBBUF_MAX];
 int usb_timeout = 1000;
 int usb_endpoint = 0x2;
 int filesize, offset;
 libusb_device **devs;
 libusb_device_handle *dev_handle;
 libusb_context *ctx = NULL;
 int r;
 ssize_t cnt;

 r = libusb_init(&ctx);
 if(r < 0 )
 {
  fprintf(stderr, "Init Error %i\n", r);
  return 1;
 }
 libusb_set_debug(ctx, 3);
 cnt = libusb_get_device_list(ctx, &devs);
 if(cnt < 0)
 {
  fprintf(stderr, "Get Device Error\n");
  return 1;
 }
 dev_handle = libusb_open_device_with_vid_pid(ctx, VENDOR_ID, PRODUCT_ID);
 if(dev_handle == NULL)
 {
  fprintf(stderr, "Cannot open device\n");
  return 1;
 }
 libusb_free_device_list(devs, 1);
 if(libusb_kernel_driver_active(dev_handle, 0) == 1)
 {
  libusb_detach_kernel_driver(dev_handle, 0);
  r = libusb_claim_interface(dev_handle, 0);
  if(r < 0)
  {
   fprintf(stderr, "Cannot Claim Interface\n");
   return 1;
  }
 }
 else
 {
  libusb_claim_interface(dev_handle, 0);
 }
 // get file size
 fseek(file, 0, SEEK_END);
 filesize = ftell(file);
 fseek(file, 0, SEEK_SET);
 // insert filesize into command
 *(int *)(usb_hdr + 4) = filesize;
 // copy header into usb buffer
 memcpy(buffer, usb_hdr, USB_HDR_LEN);
 offset = USB_HDR_LEN;
 
 while(!feof(file))
 {
  // read file into buffer
  if ((r = fread(buffer + offset, 1, URBBUF_MAX - offset, file)) < 1)
  {
   fprintf(stderr, "Error while reading file, fread returned: %d\n", r);
   break;
  }
  // pad bytes
  memset(buffer + offset + r, 0, URBBUF_MAX - offset - r);
  int actual;
  if ((r = libusb_bulk_transfer(dev_handle, usb_endpoint, buffer, URBBUF_MAX, &actual, usb_timeout)) < 0)
  {
   fprintf(stderr, "Error while writing to USB device.\n");
   fprintf(stderr, "libusb_bulk_transfer returned: %i\n", r);
  }
  // no header needed on subsequent chunks
  offset = 0;
 }
 /* rewind file */
 fseek(file, 0, SEEK_SET);
 // send keep or whatever it means signal to the device
 unsigned char data[0x00];
 r = libusb_control_transfer(dev_handle,
  0xc0,
  0x0006,
  0x0000,
  0x0000,
  data,
  0x0002,
  0);
 if (r < 0)
 {
  fprintf(stderr, "F0 error %d\n", r);
 }
 if ((unsigned int) r < sizeof(data))
 {
  fprintf(stderr, "short read (%d)\n", r);
 }
 libusb_release_interface(dev_handle, 0);
 libusb_close(dev_handle);
 libusb_exit(NULL);
 return 0;
}

int main(int argc, char **argv)
{
 FILE *file_handle;
 char *filename = NULL;
 int r;
 //char buf;
 static struct option long_options[] =
 {
  {"jpgfilename", required_argument, 0, 'j'},
  {"help",     no_argument,       0, 'h'},
 };
 int option_index = 0;
 int opt = getopt_long (argc, argv, "j:h", long_options, &option_index);
 // Check the command options
 if ( opt == -1)
 {
  show_help(argv[0]);
  exit(1);
 }
 while (opt != -1)
 {
  switch (opt)
  {
    case 'j':
     filename= optarg;
     break;
    case 'h':
     show_help(argv[0]);
     exit(0);
     break;
    default:
     abort();
     break;
  }
  opt = getopt_long (argc, argv, "j:h", long_options, &option_index);
 }
 if (optind < argc)
 {
  fprintf(stderr,"non-option elements detected: ");
  while (optind < argc)
   fprintf(stderr,"%s ", argv[optind++]);
  putchar ('\n');
  exit(1);
 }
 // file acccess begins
 if ((file_handle = fopen(filename, "r+")) == NULL)
 {
  fprintf(stderr, "File %s was not found.\n", filename);
  exit(1);
 }
 r = send_jpeg(file_handle);
 fclose(file_handle);
 if (r == 0)
  exit(0);
 else
  exit(1);

} //main
