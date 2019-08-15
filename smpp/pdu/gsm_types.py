from smpp.pdu import gsm_constants
from smpp.pdu.enum import old_style_enum as Enum
from smpp.pdu.namedtuple import namedtuple

InformationElementIdentifier = Enum(
    *list(gsm_constants.information_element_identifier_name_map.keys()))

InformationElement = namedtuple('InformationElement', 'identifier, data')

IEConcatenatedSM = namedtuple('IEConcatenatedSM', 'referenceNum, maximumNum, sequenceNum')
