import io
import struct

from smpp.pdu import gsm_constants, gsm_types
from smpp.pdu.encoding import IEncoder


class UDHParseError(Exception):
    pass


class UDHInformationElementIdentifierUnknownError(UDHParseError):
    pass


class Int8Encoder(IEncoder):

    def encode(self, value):
        return struct.pack('!B', value)

    def decode(self, file):
        byte = self.read(file, 1)
        return struct.unpack('!B', byte)[0]


class Int16Encoder(IEncoder):

    def encode(self, value):
        return struct.pack('!H', value)

    def decode(self, file):
        bytes = self.read(file, 2)
        return struct.unpack('!H', bytes)[0]


class InformationElementIdentifierEncoder(IEncoder):
    int8Encoder = Int8Encoder()
    name_map = gsm_constants.information_element_identifier_name_map
    value_map = gsm_constants.information_element_identifier_value_map

    def encode(self, value) -> bytes:
        name = str(value)
        if name not in self.name_map:
            raise ValueError("Unknown InformationElementIdentifier name %s" % name)
        return self.int8Encoder.encode(self.name_map[name])

    def decode(self, file: io.BytesIO):
        int_val = self.int8Encoder.decode(file)
        if int_val not in self.value_map:
            errStr = f'Unknown InformationElementIdentifier value {int_val}'
            raise UDHInformationElementIdentifierUnknownError(errStr)
        name = self.value_map[int_val]
        return getattr(gsm_types.InformationElementIdentifier, name)


class IEConcatenatedSMEncoder(IEncoder):
    int8Encoder = Int8Encoder()
    int16Encoder = Int16Encoder()

    def __init__(self, is16bitRefNum):
        self.is16bitRefNum = is16bitRefNum

    def encode(self, cms) -> bytes:
        bytes_ = b''
        if self.is16bitRefNum:
            bytes_ += self.int16Encoder.encode(cms.referenceNum)
        else:
            bytes_ += self.int8Encoder.encode(cms.referenceNum)
        bytes_ += self.int8Encoder.encode(cms.maximumNum)
        bytes_ += self.int8Encoder.encode(cms.sequenceNum)
        return bytes_

    def decode(self, file: io.BytesIO):
        if self.is16bitRefNum:
            ref_num = self.int16Encoder.decode(file)
        else:
            ref_num = self.int8Encoder.decode(file)
        max_num = self.int8Encoder.decode(file)
        seq_num = self.int8Encoder.decode(file)
        return gsm_types.IEConcatenatedSM(ref_num, max_num, seq_num)


class InformationElementEncoder(IEncoder):
    int8Encoder = Int8Encoder()
    iEIEncoder = InformationElementIdentifierEncoder()
    dataEncoders = {
        gsm_types.InformationElementIdentifier.CONCATENATED_SM_8BIT_REF_NUM: IEConcatenatedSMEncoder(
            False),
        gsm_types.InformationElementIdentifier.CONCATENATED_SM_16BIT_REF_NUM: IEConcatenatedSMEncoder(
            True),
    }

    def encode(self, iElement) -> bytes:
        if iElement.identifier in self.dataEncoders:
            data_bytes = self.dataEncoders[iElement.identifier].encode(iElement.data)
        else:
            data_bytes = iElement.data
        length = len(data_bytes)

        bytes_ = b''
        bytes_ += self.iEIEncoder.encode(iElement.identifier)
        bytes_ += self.int8Encoder.encode(length)
        bytes_ += data_bytes
        return bytes_

    def decode(self, file: io.BytesIO):
        fStart = file.tell()

        identifier = None
        try:
            identifier = self.iEIEncoder.decode(file)
        except UDHInformationElementIdentifierUnknownError:
            # Continue parsing after this so that these can be ignored
            pass

        length = self.int8Encoder.decode(file)
        data = None
        if identifier in self.dataEncoders:
            data = self.dataEncoders[identifier].decode(file)
        elif length > 0:
            data = self.read(file, length)

        parsed = file.tell() - fStart
        if parsed != length + 2:
            raise UDHParseError(f'Invalid length: expected {length + 2}, parsed {parsed}')

        if identifier is None:
            return None

        return gsm_types.InformationElement(identifier, data)


class UserDataHeaderEncoder(IEncoder):
    iEEncoder = InformationElementEncoder()
    int8Encoder = Int8Encoder()

    def encode(self, udh) -> bytes:
        nonRepeatable = {}
        iEBytes = b''
        for iElement in udh:
            if not self.is_identifier_repeatable(iElement.identifier):
                if iElement.identifier in nonRepeatable:
                    raise ValueError(f'Cannot repeat element {iElement.identifier}')
                for identifier in self.get_identifier_exclusion_list(iElement.identifier):
                    if identifier in nonRepeatable:
                        raise ValueError(
                            f'{iElement.identifier} and {identifier} are mutually exclusive elements'
                        )
                nonRepeatable[iElement.identifier] = None
            iEBytes += self.iEEncoder.encode(iElement)
        headerLen = len(iEBytes)
        return self.int8Encoder.encode(headerLen) + iEBytes

    # http://www.3gpp.org/ftp/Specs/archive/23_series/23.040/23040-100.zip
    # GSM spec says for non-repeatable and mutually exclusive elements that
    # get repeated we should use the last occurrance
    def decode(self, file):
        repeatable = []
        non_repeatable = {}
        header_len = self.int8Encoder.decode(file)
        while file.tell() < header_len + 1:
            iStart = file.tell()
            iElement = self.iEEncoder.decode(file)
            if iElement is not None:
                if self.is_identifier_repeatable(iElement.identifier):
                    repeatable.append(iElement)
                else:
                    non_repeatable[iElement.identifier] = iElement
                    for identifier in self.get_identifier_exclusion_list(
                            iElement.identifier):
                        if identifier in non_repeatable:
                            del non_repeatable[identifier]
            bytesRead = file.tell() - iStart
        return repeatable + list(non_repeatable.values())

    def is_identifier_repeatable(self, identifier):
        return gsm_constants.information_element_identifier_full_value_map[
            gsm_constants.information_element_identifier_name_map[str(identifier)]
        ]['repeatable']

    def get_identifier_exclusion_list(self, identifier):
        name_list = gsm_constants.information_element_identifier_full_value_map[
            gsm_constants.information_element_identifier_name_map[str(identifier)]
        ]['excludes']
        return [
            getattr(gsm_types.InformationElementIdentifier, name) for name in name_list
        ]
