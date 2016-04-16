# Copyright (C) 2009-2010 Wander Lairson Costa 
# 
# The following terms apply to all files associated
# with the software unless explicitly disclaimed in individual files.
# 
# The authors hereby grant permission to use, copy, modify, distribute,
# and license this software and its documentation for any purpose, provided
# that existing copyright notices are retained in all copies and that this
# notice is included verbatim in any distributions. No written agreement,
# license, or royalty fee is required for any of the authorized uses.
# Modifications to this software may be copyrighted by their authors
# and need not follow the licensing terms described here, provided that
# the new terms are clearly indicated on the first page of each file where
# they apply.
# 
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.

# Integraion tests

import utils
import unittest
import usb.core
import devinfo
import usb.util
import sys
import usb.backend.libusb01 as libusb01
import usb.backend.libusb10 as libusb10
import usb.backend.openusb as openusb

data_list = (utils.get_array_data1(),
             utils.get_array_data2(),
             utils.get_list_data1(),
             utils.get_list_data2(),
             utils.get_str_data1(),
             utils.get_str_data1())

class DeviceTest(unittest.TestCase):
    def __init__(self, dev):
        unittest.TestCase.__init__(self)
        self.dev = dev

    def runTest(self):
        try:
            self.test_attributes()
            self.test_timeout()
            self.test_set_configuration()
            self.test_set_interface_altsetting()
            self.test_write_read()
            self.test_ctrl_transfer()
            self.test_reset()
        finally:
            usb.util.dispose_resources(self.dev)

    def test_attributes(self):
        self.assertEqual(self.dev.bLength, 18)
        self.assertEqual(self.dev.bDescriptorType, usb.util.DESC_TYPE_DEVICE)
        self.assertEqual(self.dev.bcdUSB, 0x0200)
        self.assertEqual(self.dev.idVendor, devinfo.ID_VENDOR)
        self.assertEqual(self.dev.idProduct, devinfo.ID_PRODUCT)
        self.assertEqual(self.dev.bcdDevice, 0x0001)
        self.assertEqual(self.dev.iManufacturer, 0x01)
        self.assertEqual(self.dev.iProduct, 0x02)
        self.assertEqual(self.dev.iSerialNumber, 0x00)
        self.assertEqual(self.dev.bNumConfigurations, 0x01)
        self.assertEqual(self.dev.bMaxPacketSize0, 64)
        self.assertEqual(self.dev.bDeviceClass, 0x00)
        self.assertEqual(self.dev.bDeviceSubClass, 0x00)
        self.assertEqual(self.dev.bDeviceProtocol, 0x00)

    def test_timeout(self):
        def set_invalid_timeout():
            self.dev.default_timeout = -1
        tmo = self.dev.default_timeout
        self.dev.default_timeout = 1
        self.assertEqual(self.dev.default_timeout, 1)
        self.dev.default_timeout = tmo
        self.assertEqual(self.dev.default_timeout, tmo)
        self.assertRaises(ValueError, set_invalid_timeout)
        self.assertEqual(self.dev.default_timeout, tmo)

    def test_set_configuration(self):
        cfg = self.dev[0].bConfigurationValue
        self.dev.set_configuration(cfg)
        self.dev.set_configuration()
        self.assertEqual(cfg, self.dev.get_active_configuration().bConfigurationValue)

    def test_set_interface_altsetting(self):
        intf = self.dev.get_active_configuration()[(0,0)]
        cfg = usb.core.Configuration(self.dev).bConfigurationValue
        self.dev.set_interface_altsetting(intf.bInterfaceNumber, intf.bAlternateSetting)
        self.dev.set_interface_altsetting()

    def test_reset(self):
        self.dev.reset()
        utils.delay_after_reset()

    def test_write_read(self):
        ep_list = ((devinfo.EP_BULK_OUT, devinfo.EP_BULK_IN),
                   (devinfo.EP_INTR_OUT, devinfo.EP_INTR_IN))

        for ep in ep_list:
            for data in data_list:
                ret = self.dev.write(ep[0], data)
                self.assertEqual(ret,
                                 len(data),
                                 'Failed to write data: ' + \
                                    str(data) + ', in EP = ' + \
                                    str(ep[0])
                                )
                ret = utils.to_array(self.dev.read(ep[1], len(data)))
                self.assertEqual(ret,
                                 utils.to_array(data),
                                 str(ret) + ' != ' + \
                                    str(data) + ', in EP = ' + \
                                    str(ep[1])
                                )

    def test_ctrl_transfer(self):
        for data in data_list:
            ret = self.dev.ctrl_transfer(
                    0x40,
                    devinfo.CTRL_LOOPBACK_WRITE,
                    0,
                    0,
                    data
                )
            self.assertEqual(ret,
                             len(data),
                             'Failed to write data: ' + str(data))
            ret = utils.to_array(self.dev.ctrl_transfer(
                        0xC0,
                        devinfo.CTRL_LOOPBACK_READ,
                        0,
                        0,
                        len(data)
                    ))
            self.assertEqual(ret,
                             utils.to_array(data),
                             str(ret) + ' != ' + str(data))

class ConfigurationTest(unittest.TestCase):
    def __init__(self, dev):
        unittest.TestCase.__init__(self)
        self.cfg = dev[0]
    def runTest(self):
        try:
            self.test_attributes()
            self.test_set()
        finally:
            usb.util.dispose_resources(self.cfg.device)
    def test_attributes(self):
        self.assertEqual(self.cfg.bLength, 9)
        self.assertEqual(self.cfg.bDescriptorType, usb.util.DESC_TYPE_CONFIG)
        self.assertEqual(self.cfg.wTotalLength, 60)
        self.assertEqual(self.cfg.bNumInterfaces, 0x01)
        self.assertEqual(self.cfg.bConfigurationValue, 0x01)
        self.assertEqual(self.cfg.iConfiguration, 0x00)
        self.assertEqual(self.cfg.bmAttributes, 0xC0)
        self.assertEqual(self.cfg.bMaxPower, 50)
    def test_set(self):
        self.cfg.set()

class InterfaceTest(unittest.TestCase):
    def __init__(self, dev):
        unittest.TestCase.__init__(self)
        self.intf = dev[0][(0,0)]
    def runTest(self):
        try:
            self.test_attributes()
            self.test_set_altsetting()
        finally:
            usb.util.dispose_resources(self.intf.device)
    def test_attributes(self):
        self.assertEqual(self.intf.bLength, 9)
        self.assertEqual(self.intf.bDescriptorType, usb.util.DESC_TYPE_INTERFACE)
        self.assertEqual(self.intf.bInterfaceNumber, 0)
        self.assertEqual(self.intf.bAlternateSetting, 0)
        self.assertEqual(self.intf.bNumEndpoints, 6)
        self.assertEqual(self.intf.bInterfaceClass, 0xFF)
        self.assertEqual(self.intf.bInterfaceSubClass, 0xFF)
        self.assertEqual(self.intf.bInterfaceProtocol, 0xFF)
        self.assertEqual(self.intf.iInterface, 0x00)
    def test_set_altsetting(self):
        self.intf.set_altsetting()

class EndpointTest(unittest.TestCase):
    def __init__(self, dev):
        unittest.TestCase.__init__(self)
        dev.set_configuration()
        intf = dev[0][(0,0)]
        self.ep_out = usb.util.find_descriptor(intf, bEndpointAddress=0x01)
        self.ep_in = usb.util.find_descriptor(intf, bEndpointAddress=0x81)
    def runTest(self):
        try:
            self.test_attributes()
            self.test_write_read()
        finally:
            usb.util.dispose_resources(self.ep_out.device)
            usb.util.dispose_resources(self.ep_in.device)
    def test_attributes(self):
        self.assertEqual(self.ep_out.bLength, 7)
        self.assertEqual(self.ep_out.bDescriptorType, usb.util.DESC_TYPE_ENDPOINT)
        self.assertEqual(self.ep_out.bEndpointAddress, 0x01)
        self.assertEqual(self.ep_out.bmAttributes, 0x02)
        self.assertEqual(self.ep_out.wMaxPacketSize, 64)
        self.assertEqual(self.ep_out.bInterval, 32)
    def test_write_read(self):
        for data in data_list:
            ret = self.ep_out.write(data)
            self.assertEqual(ret, len(data), 'Failed to write data: ' + str(data))
            ret = utils.to_array(self.ep_in.read(len(data)))
            self.assertEqual(ret, utils.to_array(data), str(ret) + ' != ' + str(data))

def get_suite():
    suite = unittest.TestSuite()
    test_cases = (DeviceTest, ConfigurationTest, InterfaceTest, EndpointTest)
    for m in (libusb10, libusb01, openusb):
        b = m.get_backend()
        if b is None:
            continue
        dev = usb.core.find(backend=b,
                            idVendor=devinfo.ID_VENDOR,
                            idProduct=devinfo.ID_PRODUCT)
        if dev is None:
            utils.logger.warning('Test hardware not found for backend %s', m.__name__)
            continue

        for ObjectTestCase in test_cases:
            utils.logger.info('Adding %s(%s) to test suite...', ObjectTestCase.__name__, m.__name__)
            suite.addTest(ObjectTestCase(dev))

    return suite

if __name__ == '__main__':
    utils.run_tests(get_suite())
