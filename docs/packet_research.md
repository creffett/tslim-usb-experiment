# Introduction
The following was reverse-engineered from a USB capture of a t:connect upload of a Tandem t:slim X2. Sending data to your insulin pump is risky and could void your warranty, use this at your own risk!
# Notes
* The t:slim X2 presents itself as a USB serial interface and can be interacted with as such.
* The data is sent over the line in little-endian ordering.
* All values other than byte numbers are in hexadecimal.
* All data streams appear to begin with 0x55 (probably a sync/data notification byte), followed by a packet type identifier. All of the packet types below start at the byte following the identifier.
* The response packets appear to have the third byte be the number of bytes to follow, though it always seems to be one byte more than it should. Maybe the last byte is an uncounted checksum? Needs further investigation.
# Packet Types
## Type 0x3d
Note: Sent both as query and response type (???)
Contents: Pump serial numbers?
Sent from: Pump
Identified bytes:
* 0: probably packet length
* 1-4: Pump serial number (int)
* 5-8: Pump model number (int)
* 9-16: Unkown (10 was 0x30, rest 0x00)
* 17-20: PCBA serial number (int)
* 21-24: PCBA model number (int)
* 25-82: Unknown (27 was 0x30, rest 0x00)
* 83-92: Unknown, contained data (last six bytes looked similar to the 0x51 capture, might be timestamp)
## Type 0x51
Contents: Pump info (appears to be the contents of Settings -> My Pump -> Pump Info)
Sent from: Pump
Identified bytes:
* 0: Probably packet length
* 1-16: The ARM S/W version (string, believed to be 16 bytes - I only have 5 bytes filled)
* 17-32: The MSP S/W version (string, believed to be 16 bytes, same as above)
* 33-40: May be ConfigA and ConfigB (each int), but both are 0x00000000 for me so I can't be certain
* 41-52: Unknown, all 0x00
* 53-56: The pump serial number (int)
* 57-60: The s/w part number (int)
* 61-68: Unknown (byte 63 was 0x30 and the rest were 0x00 in my captures)
* 69-74:  PCBA serial (int)
* 75-134: Unknown, all 0x00
* 135-136: Unknown, contained data
* 137-140: Pump model (int)
* 141-146: Unknown, contained data, last three bytes changed between requests (timestamp?)
## Type 0x52
Contents: Request for pump info
Sent from: PC
Contents: `00 00 00  00 00 00 52`
