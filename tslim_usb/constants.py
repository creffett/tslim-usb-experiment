"""
Packet type 51: pump data?

Identified bytes:
0 is always 0x55, possible sync?
1 is always 0x51, presumed packet type
2 unknown
3-18 are the ARM S/W version (string, 16 byte)
19-34 are the MSP S/W version (string, 16 bytes)
55-58 are the pump serial number (int)
"""
PUMP_INFO_TYPE = 0x51
PUMP_INFO_STRUCT = '<3x16s16s20xI88x'

"""
Packet type 52: request for pump data
"""
REQUEST_PUMP_INFO_TYPE = 0x52

