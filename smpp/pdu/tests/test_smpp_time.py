import unittest
from datetime import timedelta

from smpp.pdu import smpp_time


class SMPPTimeTest(unittest.TestCase):

    def test_parse_t(self):
        self.assertEqual(0, smpp_time.parse_t('0'))
        self.assertEqual('0', smpp_time.unparse_t(0))
        self.assertEqual(9, smpp_time.parse_t('9'))
        self.assertEqual('9', smpp_time.unparse_t(9))
        self.assertRaises(ValueError, smpp_time.parse_t, 'a')
        self.assertRaises(ValueError, smpp_time.parse_t, '03')

    def test_parse_nn(self):
        self.assertEqual(0, smpp_time.parse_nn('00'))
        self.assertEqual('00', smpp_time.unparse_nn(0))
        self.assertEqual(48, smpp_time.parse_nn('48'))
        self.assertEqual('48', smpp_time.unparse_nn(48))
        self.assertRaises(ValueError, smpp_time.parse_nn, '49')
        self.assertRaises(ValueError, smpp_time.parse_nn, '0')

    def test_parse_relative(self):
        str = '020610233429000R'
        rel = smpp_time.parse(str)
        self.assertEqual(smpp_time.SMPPRelativeTime, rel.__class__)
        self.assertEqual(2, rel.years)
        self.assertEqual(6, rel.months)
        self.assertEqual(10, rel.days)
        self.assertEqual(23, rel.hours)
        self.assertEqual(34, rel.minutes)
        self.assertEqual(29, rel.seconds)
        self.assertEqual(str, smpp_time.unparse(rel))

    def test_parse_relative_mins_only(self):
        str = '000000001000000R'
        rel = smpp_time.parse(str)
        self.assertEqual(smpp_time.SMPPRelativeTime, rel.__class__)
        self.assertEqual(0, rel.years)
        self.assertEqual(0, rel.months)
        self.assertEqual(0, rel.days)
        self.assertEqual(0, rel.hours)
        self.assertEqual(10, rel.minutes)
        self.assertEqual(0, rel.seconds)
        self.assertEqual(str, smpp_time.unparse(rel))

    def test_parse_absolute_no_offset(self):
        str = '070927233429800+'
        dt = smpp_time.parse(str)
        self.assertEqual(2007, dt.year)
        self.assertEqual(9, dt.month)
        self.assertEqual(27, dt.day)
        self.assertEqual(23, dt.hour)
        self.assertEqual(34, dt.minute)
        self.assertEqual(29, dt.second)
        self.assertEqual(800000, dt.microsecond)
        self.assertEqual(None, dt.tzinfo)
        self.assertEqual(str, smpp_time.unparse(dt))

    def test_parse_absolute_positive_offset(self):
        str = '070927233429848+'
        dt = smpp_time.parse(str)
        self.assertEqual(2007, dt.year)
        self.assertEqual(9, dt.month)
        self.assertEqual(27, dt.day)
        self.assertEqual(23, dt.hour)
        self.assertEqual(34, dt.minute)
        self.assertEqual(29, dt.second)
        self.assertEqual(800000, dt.microsecond)
        self.assertEqual(timedelta(hours=12), dt.tzinfo.utcoffset(None))
        self.assertEqual(str, smpp_time.unparse(dt))

    def test_parse_absolute_negative_offset(self):
        str = '070927233429848-'
        dt = smpp_time.parse(str)
        self.assertEqual(2007, dt.year)
        self.assertEqual(9, dt.month)
        self.assertEqual(27, dt.day)
        self.assertEqual(23, dt.hour)
        self.assertEqual(34, dt.minute)
        self.assertEqual(29, dt.second)
        self.assertEqual(800000, dt.microsecond)
        self.assertEqual(timedelta(hours=-12), dt.tzinfo.utcoffset(None))
        self.assertEqual(str, smpp_time.unparse(dt))


if __name__ == '__main__':
    unittest.main()
