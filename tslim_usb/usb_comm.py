"""Class to interact with a t:slim X2 via USB."""

import struct

import serial.tools.list_ports

import packet_types

VENDOR_PRODUCT_WHITELIST = [(1155, 22336)]


def main():
    """Main loop."""

    # Find a serial port
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

    done = False
    while not done:
        print("Select an option:")
        print("  1) Request pump info")
        print("  2) Request pump serials")
        print("  0) Quit")
        selection_raw = input("Selection: ")
        try:
            selection = int(selection_raw)
        except ValueError:
            print("Invalid input {}".format(selection_raw))
            continue
        if selection == 1:
            with serial.Serial(target_port.device) as serial_port:
                write_request(serial_port, packet_types.PumpInfo.get_request_type())
                data = read_data(serial_port, packet_types.PumpInfo)
                print("\n")
                print(data)
        elif selection == 2:
            with serial.Serial(target_port.device) as serial_port:
                write_request(serial_port, packet_types.PumpSerial.get_request_type())
                data = read_data(serial_port, packet_types.PumpSerial)
                print("\n")
                print(data)
        elif selection == 0:
            done = True

    return 0


def write_request(serial_port, request_val):
    """
    Send a request to the insulin pump.

    Args:
        serial_port (:obj:`serial.Serial`): The serial port to write to.
        request_val (int): The value of the request type to use.
    """
    bytes_to_send = bytearray([0x55, request_val, 0, 0, 0, 0, 0, 0, request_val])
    serial_port.write(bytes_to_send)


def read_data(serial_port, packet_class):
    """
    Read data from the insulin pump.

    Args;
        serial_port (:obj:`serial.Serial`): The serial port to read from.
        packet_class (:obj:`class`): The class (derived from packet_types.GenericPacket)
            describing the class we expect to receive.

    Returns:
        An instance of packet_class.
    """

    if serial_port.read(1)[0] != packet_types.SYNC_BYTE:
        print("First byte wasn't the expected sync byte!")
        # Flush the serial buffer
        serial_port.reset_input_buffer()
        return None

    packet_type = serial_port.read(1)[0]
    if packet_type != packet_class.get_type():
        print("Expected packet type {:X} but got type {:X}!"
              .format(packet_class.get_type(), packet_type))
    packet_length = int(serial_port.read(1)[0])
    print("Reading {} bytes".format(packet_length))
    data = serial_port.read(packet_length)
    return packet_class._make(struct.unpack(packet_class.get_struct(), data))


if __name__ == "__main__":
    main()
