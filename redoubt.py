import argparse

from redoubt.functions import parse_type
from redoubt.instance import instance

parser = argparse.ArgumentParser()
parser.add_argument(
    '--description_file', action="store", dest="instance_file", default="instance.json", help='Instance Description File' )
parser.add_argument(
    '--itemtype', action="store", dest="itemtype", default="ec2instance"
)
parser_args = parser.parse_args()
instance_file = parser_args.instance_file

attributes = parse_type( instance_file )

region = attributes[0]["region"]
type = attributes[0]["type"]

print  attributes
if type == "ec2instance":
    new_instance = instance(region, attributes[1] )
    build = new_instance.build()