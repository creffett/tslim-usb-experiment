SYNC_BYTE = 0x55
PACKET_BYTE_STRUCT = "B"  # one byte long
PACKET_LENGTH_STRUCT = "B"  # also one byte long

"""Packet type 0x3d: pump serial numbers?"""
PUMP_SERIAL_TYPE = 0x3d
PUMP_SERIAL_STRUCT = '<II8xII66x'

"""Packet type 51: pump data"""
PUMP_INFO_TYPE = 0x51
PUMP_INFO_STRUCT = '<16s16sII12xII8xI62xI6x'

"""Packet type 52: request for pump data"""
REQUEST_PUMP_INFO_TYPE = 0x52
