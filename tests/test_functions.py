import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'../redoubt'))
import unittest
from redoubt.functions import parse_type

class UtilsTestCase(unittest.TestCase):

    def test_is_ec2instance(self):
        self.ec2file = os.path.join(os.path.dirname(__file__), 'test_ec2_instance.json')
        self.is_ec2_instance = parse_type( self.ec2file)
        self.assertEqual(self.is_ec2_instance[0]["type"], "ec2instance")

    def test_get_userdata(self):
        self.userdatafile = os.path.join(os.path.dirname(__file__), 'test_userdata.json')
        self.user_data = parse_type( self.userdatafile)
        self.assertEqual(self.is_ec2_instance[0]["type"], "ec2instance")


if __name__ == '__main__':
    unittest.main()
