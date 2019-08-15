from smpp.pdu import constants
from smpp.pdu.enum import old_style_enum as Enum
from smpp.pdu.namedtuple import namedtuple

CommandId = Enum(*list(constants.command_id_name_map.keys()))

CommandStatus = Enum(*list(constants.command_status_name_map.keys()))

Tag = Enum(*list(constants.tag_name_map.keys()))

Option = namedtuple('Option', 'tag, value')

EsmClassMode = Enum(*list(constants.esm_class_mode_name_map.keys()))
EsmClassType = Enum(*list(constants.esm_class_type_name_map.keys()))
EsmClassGsmFeatures = Enum(*list(constants.esm_class_gsm_features_name_map.keys()))

EsmClassBase = namedtuple('EsmClass', 'mode, type, gsm_features')


class EsmClass(EsmClassBase):

    def __new__(cls, mode, type, gsm_features=None):
        if gsm_features is None:
            gsm_features = []
        return EsmClassBase.__new__(cls, mode, type, set(gsm_features))

    def __repr__(self):
        return 'EsmClass[mode: %s, type: %s, gsm_features: %s]' % (
            self.mode, self.type, self.gsm_features)


RegisteredDeliveryReceipt = Enum(
    *list(constants.registered_delivery_receipt_name_map.keys()))
RegisteredDeliverySmeOriginatedAcks = Enum(
    *list(constants.registered_delivery_sme_originated_acks_name_map.keys()))

RegisteredDeliveryBase = namedtuple(
    'RegisteredDelivery', 'receipt, sme_originated_acks, intermediate_notification'
)


class RegisteredDelivery(RegisteredDeliveryBase):

    def __new__(cls, receipt, sme_originated_acks=None, intermediate_notification=False):
        if sme_originated_acks is None:
            sme_originated_acks = []
        return RegisteredDeliveryBase.__new__(cls, receipt, set(sme_originated_acks),
                                              intermediate_notification)

    def __repr__(self):
        return (f'RegisteredDelivery[receipt: {self.receipt}, '
                f'sme_originated_acks: {self.sme_originated_acks}, '
                f'intermediate_notification: {self.intermediate_notification}]')


AddrTon = Enum(*list(constants.addr_ton_name_map.keys()))
AddrNpi = Enum(*list(constants.addr_npi_name_map.keys()))
PriorityFlag = Enum(*list(constants.priority_flag_name_map.keys()))
ReplaceIfPresentFlag = Enum(*list(constants.replace_if_present_flap_name_map.keys()))

DataCodingScheme = Enum('RAW', 'DEFAULT',
                        *list(constants.data_coding_scheme_name_map.keys()))
DataCodingDefault = Enum(*list(constants.data_coding_default_name_map.keys()))
DataCodingGsmMsgCoding = Enum(
    *list(constants.data_coding_gsm_message_coding_name_map.keys()))
DataCodingGsmMsgClass = Enum(
    *list(constants.data_coding_gsm_message_class_name_map.keys()))

DataCodingGsmMsgBase = namedtuple('DataCodingGsmMsg', 'msg_coding, msg_class')


class DataCodingGsmMsg(DataCodingGsmMsgBase):

    def __new__(cls, msg_coding, msg_class):
        return DataCodingGsmMsgBase.__new__(cls, msg_coding, msg_class)

    def __repr__(self):
        return 'DataCodingGsmMsg[msg_coding: %s, msg_class: %s]' % (
            self.msg_coding, self.msg_class)


class DataCoding(object):

    def __init__(self, scheme=DataCodingScheme.DEFAULT,
                 scheme_data=DataCodingDefault.SMSC_DEFAULT_ALPHABET):
        self.scheme = scheme
        self.scheme_data = scheme_data

    def __repr__(self):
        return 'DataCoding[scheme: %s, scheme_data: %s]' % (self.scheme, self.scheme_data)

    def __eq__(self, other):
        if self.scheme != other.scheme:
            return False
        if self.scheme_data != other.scheme_data:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


DestFlag = Enum(*list(constants.dest_flag_name_map.keys()))
MessageState = Enum(*list(constants.message_state_name_map.keys()))
CallbackNumDigitModeIndicator = Enum(
    *list(constants.callback_num_digit_mode_indicator_name_map.keys()))
SubaddressTypeTag = Enum(*list(constants.subaddress_type_tag_name_map.keys()))

CallbackNumBase = namedtuple('CallbackNum', 'digit_mode_indicator, ton, npi, digits')


class CallbackNum(CallbackNumBase):

    def __new__(cls, digit_mode_indicator, ton=AddrTon.UNKNOWN, npi=AddrNpi.UNKNOWN,
                digits=None):
        return CallbackNumBase.__new__(cls, digit_mode_indicator, ton, npi, digits)

    def __repr__(self):
        return 'CallbackNum[digit_mode_indicator: %s, ton: %s, npi: %s, digits: %s]' % (
            self.digit_mode_indicator, self.ton, self.npi, self.digits)


SubaddressBase = namedtuple('Subaddress', 'type_tag, value')


class Subaddress(SubaddressBase):

    def __new__(cls, type_tag, value):
        return SubaddressBase.__new__(cls, type_tag, value)

    def __repr__(self):
        return 'Subaddress[type_tag: %s, value: %s]' % (self.type_tag, self.value)


AddrSubunit = Enum(*list(constants.addr_subunit_name_map.keys()))
NetworkType = Enum(*list(constants.network_type_name_map.keys()))
BearerType = Enum(*list(constants.bearer_type_name_map.keys()))
PayloadType = Enum(*list(constants.payload_type_name_map.keys()))
PrivacyIndicator = Enum(*list(constants.privacy_indicator_name_map.keys()))
LanguageIndicator = Enum(*list(constants.language_indicator_name_map.keys()))
DisplayTime = Enum(*list(constants.display_time_name_map.keys()))
MsAvailabilityStatus = Enum(*list(constants.ms_availability_status_name_map.keys()))
DeliveryFailureReason = Enum(*list(constants.delivery_failure_reason_name_map.keys()))
MoreMessagesToSend = Enum(*list(constants.more_messages_to_send_name_map.keys()))


class PDU(object):
    command_id = None
    mandatory_params = []
    optional_params = []

    def __init__(self, sequence_number: int = None, status=CommandStatus.ESME_ROK,
                 **kwargs):
        self.id = self.command_id
        self.sequence_number = sequence_number
        self.status = status
        self.params = kwargs
        for mParam in self.mandatory_params:
            if mParam not in self.params:
                self.params[mParam] = None

    def __repr__(self):
        r = "PDU [command: %s, sequence_number: %s, command_status: %s" % (
            self.id, self.sequence_number, self.status)
        for mParam in self.mandatory_params:
            if mParam in self.params:
                r += "\n%s: %s" % (mParam, self.params[mParam])
        for oParam in list(self.params.keys()):
            if oParam not in self.mandatory_params:
                r += "\n%s: %s" % (oParam, self.params[oParam])
        r += '\n]'
        return r

    def __eq__(self, pdu):
        if self.id != pdu.id:
            return False
        if self.sequence_number != pdu.sequence_number:
            return False
        if self.status != pdu.status:
            return False
        if self.params != pdu.params:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class PDURequest(PDU):
    require_ack = None


class PDUResponse(PDU):
    no_body_on_error = False

    def __init__(self, sequence_number: int = None, status=CommandStatus.ESME_ROK,
                 **kwargs):
        """Some PDU responses have no defined body when the status is not 0
            c.f. 4.1.4. "BIND_RECEIVER_RESP"
            c.f. 4.4.2. SMPP PDU Definition "SUBMIT_SM_RESP"
        """
        PDU.__init__(self, sequence_number, status, **kwargs)

        if self.no_body_on_error:
            if status != CommandStatus.ESME_ROK:
                self.params = {}


class PDUDataRequest(PDURequest):
    pass
