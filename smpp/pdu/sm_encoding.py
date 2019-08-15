import io
import struct
from typing import Tuple, Optional

from smpp.pdu.gsm_encoding import UserDataHeaderEncoder
from smpp.pdu.gsm_types import InformationElementIdentifier
from smpp.pdu.pdu_types import (namedtuple, DataCodingScheme, DataCodingDefault,
                                EsmClassGsmFeatures)

ShortMessageString = namedtuple('ShortMessageString', 'bytes, str, udh')


class SMStringEncoder(object):
    userDataHeaderEncoder = UserDataHeaderEncoder()

    def decode_SM(self, pdu):
        data_coding = pdu.params['data_coding']
        # TODO - when to look for message_payload instead of short_message??
        (smBytes, udhBytes, smStrBytes) = self.split_SM(pdu)
        udh = self.decode_UDH(udhBytes)

        if data_coding.scheme == DataCodingScheme.DEFAULT:
            unicode_str = None
            if data_coding.scheme_data == DataCodingDefault.SMSC_DEFAULT_ALPHABET:
                unicode_str = str(smStrBytes, 'ascii')
            elif data_coding.scheme_data == DataCodingDefault.IA5_ASCII:
                unicode_str = str(smStrBytes, 'ascii')
            elif data_coding.scheme_data == DataCodingDefault.UCS2:
                unicode_str = str(smStrBytes, 'UTF-16BE')
            elif data_coding.scheme_data == DataCodingDefault.LATIN_1:
                unicode_str = str(smStrBytes, 'latin_1')
            if unicode_str is not None:
                return ShortMessageString(smBytes, unicode_str, udh)

        raise NotImplementedError(f"I don't know what to do!!! Data coding {data_coding}")

    def contains_UDH(self, pdu):
        if EsmClassGsmFeatures.UDHI_INDICATOR_SET in pdu.params['esm_class'].gsm_features:
            return True
        return False

    def is_concatenated_SM(self, pdu):
        return self.get_concatenated_SM_info_element(pdu) is not None

    def get_concatenated_SM_info_element(self, pdu):
        (smBytes, udhBytes, smStrBytes) = self.split_SM(pdu)
        udh = self.decode_UDH(udhBytes)
        if udh is None:
            return None
        return self.find_concatenated_SM_info_element(udh)

    def find_concatenated_SM_info_element(self, udh):
        iElems = [iElem for iElem in udh if iElem.identifier in (
            InformationElementIdentifier.CONCATENATED_SM_8BIT_REF_NUM,
            InformationElementIdentifier.CONCATENATED_SM_16BIT_REF_NUM
        )]
        assert len(iElems) <= 1
        if len(iElems) == 1:
            return iElems[0]
        return None

    def decode_UDH(self, udhBytes: bytes):
        if udhBytes is not None:
            return self.userDataHeaderEncoder.decode(io.BytesIO(udhBytes))
        return None

    def split_SM(self, pdu) -> Tuple[bytes, Optional[bytes], bytes]:
        short_message: bytes = pdu.params['short_message']
        if self.contains_UDH(pdu):
            if len(short_message) == 0:
                raise ValueError("Empty short message")
            header_len = struct.unpack('!B', short_message[0:1])[0]
            if header_len + 1 > len(short_message):
                raise ValueError(
                    f'Invalid header len ({header_len}). Longer than short_message len ({len(short_message)}) + 1')
            return (
                short_message,
                short_message[:header_len + 1],
                short_message[header_len + 1:]
            )
        return short_message, None, short_message
