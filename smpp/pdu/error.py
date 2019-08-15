from smpp.pdu import constants


class SMPPError(Exception):
    """Base class for SMPP errors
    """


class SMPPClientError(SMPPError):
    """Raised for client-side errors
    """


class SMPPClientConnectionCorruptedError(SMPPClientError):
    """Raised when operations are attempted after the client has received corrupt data
    """


class SMPPClientSessionStateError(SMPPClientError):
    """Raised when illegal operations are attempted for the client's session state
    """


class SMPPTransactionError(SMPPError):
    """Raised for transaction errors
    """

    def __init__(self, response, request=None):
        self.response = response
        self.request = request
        SMPPError.__init__(self, self.get_error_str())

    def get_error_str(self):
        err_code_name = str(self.response.status)
        err_code_val = constants.command_status_name_map[err_code_name]
        err_code_desc = constants.command_status_value_map[err_code_val]
        return f'{err_code_name} ({err_code_desc})'


class SMPPGenericNackTransactionError(SMPPTransactionError):
    """Raised for transaction errors that return generic_nack
    """


class SMPPRequestTimoutError(SMPPError):
    """Raised for timeout waiting waiting for response
    """


class SMPPSessionInitTimoutError(SMPPRequestTimoutError):
    """Raised for timeout waiting waiting for response
    """


class SMPPProtocolError(SMPPError):
    """Raised for SMPP protocol errors
    """

    def __init__(self, err_str, command_status):
        self.status = command_status
        SMPPError.__init__(self, f'{self.get_status_description()}: {err_str}')

    def get_status_description(self):
        int_val = constants.command_status_name_map[str(self.status)]
        return constants.command_status_value_map[int_val]['description']


class SessionStateError(SMPPProtocolError):
    """Raise when illegal operations are received for the given session state
    """


class PDUParseError(SMPPProtocolError):
    """Parent class for PDU parsing errors
    """


class PDUCorruptError(PDUParseError):
    """Raised when a complete PDU cannot be read from the network
    """
