import struct

import serial.tools.list_ports

import constants

VENDOR_PRODUCT_WHITELIST = [(1155, 22336)]


def main():
    target_port = None
    for port in list(serial.tools.list_ports.comports()):
        if (port.vid, port.pid) in VENDOR_PRODUCT_WHITELIST:
            if target_port is not None:
                print("More than one port matches the desired vendor/product pairing,"
                      "can't figure out which to use!")
                return 1
            target_port = port

    if target_port is None:
        print("Couldn't find a suitable connected device. Exiting.")
        return 1
    with serial.Serial(target_port.device) as serial_port:
        write_request(constants.PUMP_SERIAL_TYPE, serial_port)
        first_byte = struct.unpack(constants.PACKET_BYTE_STRUCT, serial_port.read(1))
        if first_byte[0] != constants.SYNC_BYTE:
            print("Unexpected data {:X}!".format(first_byte[0]))
            return 1
        read_data(serial_port)


def write_request(request_val, serial_port):
    ba = bytearray([0x55, request_val, 0, 0, 0, 0, 0, 0, request_val])
    serial_port.write(ba)


def read_data(serial_port):
    packet_type = serial_port.read(1)
    _ = serial_port.read(1)  # data length, to be used in the future
    if packet_type[0] == constants.PUMP_INFO_TYPE:
        data = struct.unpack(constants.PUMP_INFO_STRUCT,
                             serial_port.read(struct.calcsize(constants.PUMP_INFO_STRUCT)))
        print(data)
    elif packet_type[0] == constants.PUMP_SERIAL_TYPE:
        data = struct.unpack(constants.PUMP_SERIAL_STRUCT,
                             serial_port.read(struct.calcsize(constants.PUMP_SERIAL_STRUCT)))
        print(data)
    else:
        print("Unknown packet type 0x{:X}!".format(packet_type))


if __name__ == "__main__":
    main()
