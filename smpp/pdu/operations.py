from smpp.pdu.pdu_types import CommandId, PDU, PDURequest, PDUResponse, PDUDataRequest


class BindTransmitterResp(PDUResponse):
    no_body_on_error = True
    command_id = CommandId.bind_transmitter_resp
    mandatory_params = ['system_id']
    optional_params = ['sc_interface_version']


class BindTransmitter(PDURequest):
    require_ack = BindTransmitterResp
    command_id = CommandId.bind_transmitter
    mandatory_params = [
        'system_id',
        'password',
        'system_type',
        'interface_version',
        'addr_ton',
        'addr_npi',
        'address_range',
    ]


class BindReceiverResp(PDUResponse):
    no_body_on_error = True
    command_id = CommandId.bind_receiver_resp
    mandatory_params = ['system_id']
    optional_params = ['sc_interface_version']


class BindReceiver(PDURequest):
    require_ack = BindReceiverResp
    command_id = CommandId.bind_receiver
    mandatory_params = [
        'system_id',
        'password',
        'system_type',
        'interface_version',
        'addr_ton',
        'addr_npi',
        'address_range',
    ]


class BindTransceiverResp(PDUResponse):
    no_body_on_error = True
    command_id = CommandId.bind_transceiver_resp
    mandatory_params = ['system_id']
    optional_params = ['sc_interface_version']


class BindTransceiver(PDURequest):
    require_ack = BindTransceiverResp
    command_id = CommandId.bind_transceiver
    mandatory_params = [
        'system_id',
        'password',
        'system_type',
        'interface_version',
        'addr_ton',
        'addr_npi',
        'address_range',
    ]


class Outbind(PDU):
    command_id = CommandId.outbind
    mandatory_params = [
        'system_id',
        'password',
    ]


class UnbindResp(PDUResponse):
    command_id = CommandId.unbind_resp


class Unbind(PDURequest):
    require_ack = UnbindResp
    command_id = CommandId.unbind


class GenericNack(PDUResponse):
    command_id = CommandId.generic_nack


class SubmitSMResp(PDUResponse):
    no_body_on_error = True
    command_id = CommandId.submit_sm_resp
    mandatory_params = ['message_id']


class SubmitSM(PDUDataRequest):
    require_ack = SubmitSMResp
    command_id = CommandId.submit_sm
    mandatory_params = [
        'service_type',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'dest_addr_ton',
        'dest_addr_npi',
        'destination_addr',
        'esm_class',
        'protocol_id',
        'priority_flag',
        'schedule_delivery_time',
        'validity_period',
        'registered_delivery',
        'replace_if_present_flag',
        'data_coding',
        'sm_default_msg_id',
        # The sm_length parameter is handled by ShortMessageEncoder
        'short_message',
    ]
    optional_params = [
        'user_message_reference',
        'source_port',
        'source_addr_subunit',
        'destination_port',
        'dest_addr_subunit',
        'sar_msg_ref_num',
        'sar_total_segments',
        'sar_segment_seqnum',
        'more_messages_to_send',
        'payload_type',
        'message_payload',
        'privacy_indicator',
        'callback_num',
        'callback_num_pres_ind',
        'callback_num_atag',
        'source_subaddress',
        'dest_subaddress',
        'user_response_code',
        'display_time',
        'sms_signal',
        'ms_validity',
        'ms_msg_wait_facilities',
        'number_of_messages',
        'alert_on_msg_delivery',
        'language_indicator',
        'its_reply_type',
        'its_session_info',
        'ussd_service_op',
    ]


class SubmitMultiResp(PDUResponse):
    command_id = CommandId.submit_multi_resp
    mandatory_params = [
        'message_id',
        'no_unsuccess',
        'no_unsuccess_sme',
    ]


class SubmitMulti(PDUDataRequest):
    require_ack = SubmitMultiResp
    command_id = CommandId.submit_multi
    mandatory_params = [
        'service_type',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'number_of_dests',
        'dest_address',
        'esm_class',
        'protocol_id',
        'priority_flag',
        'schedule_delivery_time',
        'validity_period',
        'registered_delivery',
        'replace_if_present_flag',
        'data_coding',
        'sm_default_msg_id',
        # The sm_length parameter is handled by ShortMessageEncoder
        'short_message',
    ]
    optional_params = [
        'user_message_reference',
        'source_port',
        'source_addr_subunit',
        'destination_port',
        'dest_addr_subunit',
        'sar_msg_ref_num',
        'sar_total_segments',
        'sar_segment_seqnum',
        'more_messages_to_send',
        'payload_type',
        'message_payload',
        'privacy_indicator',
        'callback_num',
        'callback_num_pres_ind',
        'callback_num_atag',
        'source_subaddress',
        'dest_subaddress',
        'display_time',
        'sms_signal',
        'ms_validity',
        'ms_msg_wait_facilities',
        'number_of_messages',
        'alert_on_msg_delivery',
        'language_indicator',
    ]


class DeliverSMResp(PDUResponse):
    command_id = CommandId.deliver_sm_resp
    mandatory_params = ['message_id']


class DeliverSM(PDUDataRequest):
    require_ack = DeliverSMResp
    command_id = CommandId.deliver_sm
    mandatory_params = [
        'service_type',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'dest_addr_ton',
        'dest_addr_npi',
        'destination_addr',
        'esm_class',
        'protocol_id',
        'priority_flag',
        'schedule_delivery_time',
        'validity_period',
        'registered_delivery',
        'replace_if_present_flag',
        'data_coding',
        'sm_default_msg_id',
        # The sm_length parameter is handled by ShortMessageEncoder
        'short_message',
    ]
    optional_params = [
        'user_message_reference',
        'source_port',
        'destination_port',
        'sar_msg_ref_num',
        'sar_total_segments',
        'sar_segment_seqnum',
        'user_response_code',
        'privacy_indicator',
        'payload_type',
        'message_payload',
        'callback_num',
        'source_subaddress',
        'dest_subaddress',
        'language_indicator',
        'its_session_info',
        'network_error_code',
        'message_state',
        'receipted_message_id',
    ]


class DataSMResp(PDUResponse):
    command_id = CommandId.data_sm_resp
    mandatory_params = ['message_id']
    optional_params = [
        'delivery_failure_reason',
        'network_error_code',
        'additional_status_info_text',
        'dpf_result',
    ]


class DataSM(PDUDataRequest):
    require_ack = DataSMResp
    command_id = CommandId.data_sm
    mandatory_params = [
        'service_type',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'dest_addr_ton',
        'dest_addr_npi',
        'destination_addr',
        'esm_class',
        'registered_delivery',
        'data_coding',
    ]
    optional_params = [
        'source_port',
        'source_addr_subunit',
        'source_network_type',
        'source_bearer_type',
        'source_telematics_id',
        'destination_port',
        'dest_addr_subunit',
        'dest_network_type',
        'dest_bearer_type',
        'dest_telematics_id',
        'sar_msg_ref_num',
        'sar_total_segments',
        'sar_segment_seqnum',
        'more_messages_to_send',
        'qos_time_to_live',
        'payload_type',
        'message_payload',
        'set_dpf',
        'receipted_message_id',
        'message_state',
        'network_error_code',
        'user_message_reference',
        'privacy_indicator',
        'callback_num',
        'callback_num_pres_ind',
        'callback_num_atag',
        'source_subaddress',
        'dest_subaddress',
        'user_response_code',
        'display_time',
        'sms_signal',
        'ms_validity',
        'ms_msg_wait_facilities',
        'number_of_messages',
        'alert_on_msg_delivery',
        'language_indicator',
        'its_reply_type',
        'its_session_info',
    ]


class QuerySMResp(PDUResponse):
    command_id = CommandId.query_sm_resp
    mandatory_params = [
        'message_id',
        'final_date',
        'message_state',
        'error_code',
    ]


class QuerySM(PDUDataRequest):
    require_ack = QuerySMResp
    command_id = CommandId.query_sm
    mandatory_params = [
        'message_id',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
    ]


class CancelSMResp(PDUResponse):
    command_id = CommandId.cancel_sm_resp


class CancelSM(PDUDataRequest):
    require_ack = CancelSMResp
    command_id = CommandId.cancel_sm
    mandatory_params = [
        'service_type',
        'message_id',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'dest_addr_ton',
        'dest_addr_npi',
        'destination_addr',
    ]


class ReplaceSMResp(PDUResponse):
    command_id = CommandId.replace_sm_resp


class ReplaceSM(PDUDataRequest):
    require_ack = ReplaceSMResp
    command_id = CommandId.replace_sm
    mandatory_params = [
        'message_id',
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'schedule_delivery_time',
        'validity_period',
        'registered_delivery',
        'sm_default_msg_id',
        'sm_length',
        'short_message',
    ]


class EnquireLinkResp(PDUResponse):
    command_id = CommandId.enquire_link_resp


class EnquireLink(PDURequest):
    require_ack = EnquireLinkResp
    command_id = CommandId.enquire_link


class AlertNotification(PDU):
    command_id = CommandId.alert_notification
    mandatory_params = [
        'source_addr_ton',
        'source_addr_npi',
        'source_addr',
        'esme_addr_ton',
        'esme_addr_npi',
        'esme_addr',
    ]
    optional_params = [
        'ms_availability_status',
    ]


PDUS = {}


def _register():
    for pduKlass in list(globals().values()):
        try:
            if issubclass(pduKlass, PDU):
                PDUS[pduKlass.command_id] = pduKlass
        except TypeError:
            pass


_register()


def get_pdu_class(command_id):
    return PDUS[command_id]
