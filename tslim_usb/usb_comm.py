import struct

import serial.tools.list_ports

import constants

VENDOR_PRODUCT_WHITELIST = [(1155, 22336)]


def main():
    target_port = None
    for port in list(serial.tools.list_ports.comports()):
        if (port.vid, port.pid) in VENDOR_PRODUCT_WHITELIST:
            if target_port is not None:
                print("More than one port matches the desired vendor/product pairing, can't figure out which to use!")
                return 1
            target_port = port

    if target_port is None:
        print("Couldn't find a suitable connected device. Exiting.")
        return 1
    with serial.Serial(target_port.device) as serial_port:
        write_request(constants.REQUEST_PUMP_INFO_TYPE, serial_port)
        data = struct.unpack(constants.PUMP_INFO_STRUCT,
                             serial_port.read(struct.calcsize(constants.PUMP_INFO_STRUCT)))
        print("Detected a t:slim X2 with serial number {}".format(data[2]))


def write_request(request_val, port):
    ba = bytearray([0x55, request_val, 0, 0, 0, 0, 0, 0, request_val])
    port.write(ba)


if __name__ == "__main__":
    main()
