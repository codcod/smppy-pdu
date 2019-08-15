import io
from typing import Any

from smpp.pdu import pdu_types
from smpp.pdu.error import PDUCorruptError


class IEncoder(object):

    def encode(self, value: Any) -> bytes:
        """Takes an object representing the type and returns a byte string"""
        raise NotImplementedError()

    def decode(self, file: io.BytesIO) -> Any:
        """Takes file stream in and returns an object representing the type"""
        raise NotImplementedError()

    def read(self, file: io.BytesIO, size: int):
        bytes_read = file.read(size)
        length = len(bytes_read)
        if length == 0:
            raise PDUCorruptError("Unexpected EOF",
                                  pdu_types.CommandStatus.ESME_RINVMSGLEN)
        if length != size:
            raise PDUCorruptError(
                "Length mismatch. Expecting %d bytes. Read %d" % (size, length),
                pdu_types.CommandStatus.ESME_RINVMSGLEN)
        return bytes_read
