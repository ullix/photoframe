/* $Id: spf87h-tool,v 0.1 2011/01/15 22:11:54i */
/* Use only with the Samsung SPF-87H. */
/* No commercial affiliation, warranty, copyright, party invitation, */
/* fitness or non-fitness, implied or otherwise, is claimed by this comment. */
/* Compile with make. */


#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <string.h>
#include <fcntl.h>
#include </home/ullix/websites/local/photoframe/spf87h-tool-v0.01/usb.h>

#include <libusb-1.0/libusb.h>

#define SPF87H_VID      0x04e8
#define SPF87H_PID1     0x2033
#define SPF87H_PID2     0x2034
libusb_device * find_spf(libusb_device **devs) {
	libusb_device *dev; //target device reference
	int i = 0;

	while ((dev = devs[i++]) != NULL) {
		struct libusb_device_descriptor desc; //target device description
		int r = libusb_get_device_descriptor(dev, &desc);
		if (r < 0) {
			fprintf(stderr, "failed to get device descriptor");
			return NULL;
		}
		if(desc.idVendor == SPF87H_VID) {
	 		if(desc.idProduct == SPF87H_PID1 ||
			   desc.idProduct == SPF87H_PID2) {
			   	fprintf(stderr, "Samsung SPF-87H ");
				if(desc.idProduct == SPF87H_PID1) {
					fprintf(stderr, "in Mass Storage Mode found\n");
					fprintf(stderr, "Change to Mini Monitor Mode and retry\n");
                			libusb_free_device_list(devs, 1);
		                	libusb_exit(NULL);
				        return NULL;

				}
				else {
					fprintf(stderr, "in Monitor Mode found\n");
				}
				return dev;
			}
		}
	}
	return NULL;
}

int main(void) {
    
	libusb_device **devs; //a list of usb devices
	libusb_device *dev; //target device reference
	struct libusb_device_handle *devh = NULL;
	int r;
	ssize_t cnt;

	r = libusb_init(NULL);
	if (r < 0)
	{
		fprintf(stderr, "failed to initialize libusb\n");
		 return r;
	}

	libusb_set_debug(NULL,3); // set Debug Level

	cnt = libusb_get_device_list(NULL, &devs);
	if (cnt < 0) {
		fprintf(stderr, "No usb devices found\n");
		libusb_free_device_list(devs, 1);
		libusb_exit(NULL);
		return cnt;
	}

	dev=find_spf(devs); // find our device
	if(!dev) {
		fprintf(stderr, "Suitable Samsung SPF-87H not found\n");
		return -1;
	}
	
	r = libusb_open(dev,&devh); // open the device handle
	if(r!=0) {
		fprintf(stderr, "Error opening device\n");
		fprintf(stderr, "No mode setting possible\n");
		libusb_free_device_list(devs, 1);
		libusb_exit(NULL);
		return -1;
	}
	r = libusb_claim_interface(devh, 0); // claiming the device
	if (r < 0) {
		fprintf(stderr, "usb_claim_interface error %d %s\n", r, strerror(-r));
		fprintf(stderr, "trying to detach from system...");
		r = libusb_detach_kernel_driver(devh, 0);
		if (r < 0) {
			fprintf(stderr, "\nDetaching from system failed, goodbye\n");
			libusb_free_device_list(devs, 1);
			libusb_exit(NULL);
			return -1;
		}
		else {
			fprintf(stderr, " successfully\n");
			r = libusb_claim_interface(devh, 0);
			if (r < 0) {
				fprintf(stderr, "usb_claim_interface error %d %s remains, giving up\n", r, strerror(-r));
				libusb_free_device_list(devs, 1);
				libusb_exit(NULL);
				return -1;
			}
			else {
				fprintf(stderr, "claimed interface\n");
			}
		}
	}
	else {
		printf("claimed interface\n");
	}

	fprintf(stderr, "Sending Mini Monitor Mode command sequence...");

	// sequence 1/9
	int actual_length;
	actual_length=-1;
	unsigned char adata[0x0];
	unsigned char bdata[0x00];
	r = libusb_control_transfer(devh,
				 0xc0,    //uint8_t  bmRequestType,
				 4,       //uint8_t  bRequest,
				 0x0000,  //uint16_t wValue,
				 0,       //uint16_t wIndex,
				 adata,    //unsigned char *data
				 1,      //uint16_t  wLength,
				 0);    //unsigned int timeout
	if (r < 0) {
		fprintf(stderr, "F0 error %d\n", r);
	}
	if ((unsigned int) r < sizeof(adata)) {
		fprintf(stderr, "short read (%d)\n", r);
	}

	int i;
	for (i=1;i<6;i++) {
		// sequence 2/9 - 8/9
		actual_length=-1;
		r = libusb_control_transfer(devh,
					 0xc0,    //uint8_t  bmRequestType,
					 1,       //uint8_t  bRequest,
					 0x0000,  //uint16_t wValue,
					 0,       //uint16_t wIndex,
					 bdata,    //unsigned char *data
					 2,      //uint16_t  wLength,
					 0);    //unsigned int timeout
		if (r < 0) {
			fprintf(stderr, "F0 error %d\n", r);
		}
		if ((unsigned int) r < sizeof(adata)) {
			fprintf(stderr, "short read (%d)\n", r);
		}
	}
	
	// sequence 9/9
	actual_length=-1;
	r = libusb_control_transfer(devh,
				 0xc0,    //uint8_t  bmRequestType,
				 6,       //uint8_t  bRequest,
				 0x0000,  //uint16_t wValue,
				 0,       //uint16_t wIndex,
				 bdata,    //unsigned char *data
				 2,      //uint16_t  wLength,
				 0);    //unsigned int timeout
	if (r < 0) {
		fprintf(stderr, "F0 error %d\n", r);
	}
	if ((unsigned int) r < sizeof(adata)) {
		fprintf(stderr, "short read (%d)\n", r);
	}

	fprintf(stderr, " finished.\n");

	libusb_release_interface(devh, 0);
	libusb_close(devh);
	libusb_free_device_list(devs, 1);
	libusb_exit(NULL);

	fprintf(stderr, "Done.\n");
	return 0;
}

