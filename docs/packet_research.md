# Packet Types
## Type 0x51
Contents: Pump info (appears to be the contents of Settings -> My Pump -> Pump Info)
Sent from: Pump
Identified bytes:
* 0 is always 0x55, possible sync?
* 1 is always 0x51, packet type
* 2 unknown
* 3-18 are the ARM S/W version (string, believed to be 16 bytes)
* 19-34 are the MSP S/W version (string, believed to be 16 bytes)
* 55-58 are the pump serial number (int)
## Type 0x52
Contents: Request for pump info
Sent from: PC
