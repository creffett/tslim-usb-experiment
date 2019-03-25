import typing
from abc import ABCMeta, abstractmethod

SYNC_BYTE = 0x55


class GenericPacket(metaclass=ABCMeta):
    """Methods common to all packets."""

    @classmethod
    @abstractmethod
    def get_type(cls):
        """Override this with a return of the class's type byte."""
        ...

    @classmethod
    @abstractmethod
    def get_request_type(cls):
        """Override this with a return of the class's request type byte."""
        ...

    @classmethod
    @abstractmethod
    def get_struct(cls):
        """Override this with a return of the class's struct."""
        ...


class IntermediaryMeta(type(GenericPacket), type(typing.NamedTuple)):
    """Intermediary metaclass to fix multiple-metaclass issues...yuck."""
    pass


class PumpInfo(GenericPacket, typing.NamedTuple, metaclass=IntermediaryMeta):
    """
    The contents of packet type 0x51 (Pump Info)

    Attributes:
        arm (str): Value of the ARM S/W field
        msp (str): Value of the MSP S/W field
        config_a (int): Value of the ConfigA Bits field
        config_b (int): Value of the ConfigB Bits field
        sw_part_number (int): Value of the S/W Part Number field
        serial (int): Pump serial number
        pcba_serial (int): PCBA serial number
        pump_model (int): Pump model number
    """

    arm: str
    msp: str
    config_a: int
    config_b: int
    pump_serial: int
    sw_part_number: int
    pcba_serial: int
    pump_model: int

    # Class overrides
    @classmethod
    def get_type(cls):
        return 0x51

    @classmethod
    def get_request_type(cls):
        return 0x52

    @classmethod
    def get_struct(cls):
        return '<16s16sII12xII8xI62xI'

    def __str__(self):
        ret = "Packet type {:X} (Pump Info):\n".format(self.get_type())
        ret += "  Pump serial number: {}\n".format(self.pump_serial)
        ret += "  Pump model number: {}\n".format(self.pump_model)
        ret += "  ARM S/W: {}\n".format(self.arm.decode('ascii'))
        ret += "  MSP S/W: {}\n".format(self.msp.decode('ascii'))
        ret += "  Config A bits: 0x{:08X}\n".format(self.config_a)
        ret += "  Config B bits: 0x{:08X}\n".format(self.config_b)
        ret += "  PCBA serial: {}\n".format(self.pcba_serial)
        ret += "  S/W part number: {}\n".format(self.sw_part_number)
        return ret


class PumpSerial(GenericPacket, typing.NamedTuple, metaclass=IntermediaryMeta):
    """
    The contents of packet type 0x3d (Pump Serial)

    Attributes:
        pump_serial (int): Pump serial number
        pump_model (int): Pump model number
        pcba_serial (int): PCBA serial number
        pcba_model (int): PCBA model number
    """

    pump_serial: int
    pump_model: int
    pcba_serial: int
    pcba_model: int

    # Class overrides
    @classmethod
    def get_type(cls):
        """Override."""
        return 0x3d

    @classmethod
    def get_request_type(cls):
        """Override, yes, the request and return are the same here."""
        return 0x3d

    @classmethod
    def get_struct(cls):
        return '<II8xII60x'

    def __str__(self):
        ret = "Packet type {:X} (Pump serial numbers:\n".format(self.get_type())
        ret += "  Pump serial number: {}\n".format(self.pump_serial)
        ret += "  Pump model number: {}\n".format(self.pump_model)
        ret += "  PCBA serial: {}\n".format(self.pcba_serial)
        ret += "  PCBA model: {}\n".format(self.pcba_model)
        return ret
