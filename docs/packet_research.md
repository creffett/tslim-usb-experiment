# Introduction
The following was reverse-engineered from a USB capture of a t:connect upload of a Tandem t:slim X2. Sending data to your insulin pump is risky and could void your warranty, use this at your own risk!

# Notes
* The t:slim X2 presents itself as a USB serial interface and can be interacted with as such.
* The data is sent over the line in little-endian ordering.
* All values below other than byte numbers are in hexadecimal, byte numbers are zero-indexed.
* All data streams appear to begin with 0x55 (probably a sync/data notification byte), followed by a packet type identifier, followed by a length field. All of the packet types below start at the byte following the length field.
* Response packets also all end with a similar 6-byte sequence - an invariant (changed per session) followed by three variable bytes. I suspect the latter three bytes are some sort of sum of all bytes after the 0x55 (possibly with a modulo) - this guess comes from the requests, where the last byte is either the same as the packet type or that plus the additional request field (if there is one)

# Packet Types
## Type 0x3d
Note: Sent both as query and response type (???)
Contents: Pump serial numbers?
Sent from: Pump
Identified bytes:
* 0-3: Pump serial number (int)
* 4-7: Pump model number (int)
* 8-15: Unknown (9 was 0x30, rest 0x00)
* 16-19: PCBA serial number (int)
* 20-23: PCBA model number (int)
* 24-81: Unknown (26 was 0x30, rest 0x00)

## Type 0x51
Contents: Pump info (appears to be the contents of Settings -> My Pump -> Pump Info)
Sent from: Pump
Identified bytes:
* 0-15: The ARM S/W version (string, believed to be 16 bytes - I only have 5 bytes filled)
* 16-31: The MSP S/W version (string, believed to be 16 bytes, same as above)
* 32-39: May be ConfigA and ConfigB (each int), but both are 0x00000000 for me so I can't be certain
* 40-51: Unknown, all 0x00
* 52-55: The pump serial number (int)
* 56-59: The s/w part number (int)
* 60-67: Unknown (byte 63 was 0x30 and the rest were 0x00 in my captures)
* 68-71:  PCBA serial (int)
* 72-133: Unknown, all 0x00
* 134-135: Unknown, contained data
* 136-139: Pump model (int)

## Type 0x52
Contents: Request for pump info
Sent from: PC
Length: 0

## Type 0xad
Contents: unknown request
Sent from: PC
Length: 0

## Type 0xae
Contents: unknown
Sent from: Pump
Identified bytes:
* 0-5: Unknown, byte 0 was 0x01 and the rest were 0x00

## Type 0xaf
Contents: Personal profiles request
Sent from: PC
Length: 1
Note: Has a single byte of value (very likely an index into the list of personal profiles), seen values of 0x00-0x05

## Type 0xb0
Contents: Personal profiles
Sent from: Pump
Length: Variable
Notes: I occasionally saw the same timeslot twice but with different data - further investigation pending.
Identified bytes:
* 0: Unknown (0x00)
* 1-17: Profile name (string, matches pump behavior - max profile name is 17 characters)
* 18: Number of timeslots
* 19: First timeslot
* 32: Second timeslot
* 45: Third timeslot
* 58: Fourth timeslot
* 71: Fifth timeslot
* 84: Sixth timeslot
* 97: Seventh timeslot
* 110: Eighth timeslot
* 123: Ninth timeslot
* 136: Tenth timeslot
* 149: Eleventh timeslot
* 162: Twelfth timeslot
* 175: Thirteenth timeslot
* 188: Fourteenth timeslot
* 201: Fifteenth timeslot
* 214: Sixteenth timeslot
* 227-228: Insulin duration time in minutes (unsigned short)
* 229-230: Max bolus * 1000 (unsigned short)
* 231: Possibly carbohydrates on/off (bool)
* 232: Unknown

### Profile timeslot data structure
13 bytes
Note: Unused timeslots are filled with 0xff
Bytes:
* 0-1: Time in minutes since 12:00 AM (unsigned short)
* 4-5: Carbs/unit insulin * 1000 (unsigned short)
* 6-7: Unknown (both were always 0x00 in my data)
* 8: Target BG (unsigned char)
* 9-10: Correction factor (unsigned short)
* 11-12: Unknown (was the same data as correction factor for me)

### Empty profile data
2 bytes
Note: Seen two combinations: `af 00` and `c6 00`, the latter was used on the last empty profile.

## Type 0xb2
Contents: Pump settings request
Sent from: PC
Length: 0

## Type 0xb3
Contents: Pump settings
Sent from: Pump
Notes: I suspect that this packet also contains quick bolus on/off and quick bolus increment time, but I haven't identified the bytes.
Bytes:
* Byte 2: Screen timeout (1 byte, see below)
* Byte 6: Quick bolus increment (1 byte, number of units, 0x00 signifies .5 units)
* Byte 7: Button volume (1 byte, see below)
* Byte 8: Quick bolus volume (1 byte, see below)
* Byte 9: Bolus volume (1 byte, see below)
* Byte 10: Reminders volume (1 byte, see below)
* Byte 11: Alerts volume (1 byte, see below)
* Byte 12: Alarm volume (1 byte, see below)

### Screen timeout enum
* 0: 15s
* 1: 30s
* 2: 60s
* 3: 120s
### Volume enum
* 0: High
* 1: Medium
* 2: Low
* 3: Vibrate

## Type 0xb8
Contents: Unidentified request (possibly alert settings)
Sent from: PC
Length: 0

## Type: 0xb9
Contents: Unidentified (possibly alert settings)
Sent from: Pump

## Type: 0xb5
Contents: Unidentified request
Sent from: PC
Length: 0

## Type: 0xb6
Contents: Unidentified
Sent from: Pump
Identified bytes:
* 15-22: String (contained the word "INSULIN" in my capture)

## Type: 0xa8

## Type: 0xa9
Contents: Unidentified
Sent from: Pump


## Type: 0x98
Contents: Request for history dump
Sent from: PC
Length: 8
Note: Contents still under investigation, suspected to be a start date or the like.

## Type: 0x7d
Contents: Pump history?
Identified bytes:
0-1: Sequence number, went up for each packet received in the history dump (unsigned short).
2-5: Invariant, probably part of the above sequence number.

