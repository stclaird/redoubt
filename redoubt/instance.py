from aws import aws
from functions import user_data_build

class instance ( aws ):

    def __init__( self, region, attributes ):
        super ( instance , self ).__init__( region )
        self.instance_data = self.parse_attributes( attributes )

    def parse_attributes(self, attributes ):

        instance_meta = {}
        instance_meta["host_name"] = attributes.get('host_name', 'buildserver')
        instance_meta["waiter"] = attributes.get('waiter', None)
        instance_meta["elb_name"] = attributes.get('elb_name', None)
        instance_meta["security_groups"] = attributes.get("security_groups", None)

        instance={}
        instance["MinCount"]=1
        instance["MaxCount"]=1
        instance["DryRun"]=False
        instance["ImageId"]=attributes.get('ami_id')
        instance["NetworkInterfaces"]= [{
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': attributes.get('assign_public_ip', False),
            'SubnetId': attributes.get("subnet_id")
        }]
        instance["KeyName"]=attributes.get('key_name')
        instance["InstanceType"]=attributes.get('instance_type', "t2.micro")
        instance["EbsOptimized"]=attributes.get('EbsOptimized', False)

        if attributes.get('IamInstanceProfile') != None:
            instance["IamInstanceProfile"] = {'Name': attributes.get('iam_profile')}

        if attributes.get('private_ip') != None:
           instance["private_ip"] = attributes.get('private_ip')

        if attributes.get('Placement,') != None:
           instance["Placement,"] = attributes.get('placement_group')

        instance["BlockDeviceMappings"] = attributes.get('block_devices', [{
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "VolumeSize": 24,
                "VolumeType": "standard",
                "DeleteOnTermination": True
            }
        }])

        instance["UserData"] = user_data_build( attributes.get('host_name'), attributes.get('user_data_snippets') )

        return [ instance_meta, instance ]

    def build (self):

        new_attribs = self.instance_data[1]
        print new_attribs
        new_instance = self.ec2_resource.create_instances(**new_attribs)

        instance = self.ec2_resource.Instance(new_instance[0].id)

        self.create_tag(instance, "Name", self.instance_data[0]["host_name"] )

        if self.instance_data[0]["security_groups"] != None:
            instance.modify_attribute(Groups=self.instance_data[0]["security_groups"])

        instance = self.ec2_resource.Instance(new_instance[0].id)
        instance_ip = instance.private_ip_address

        return [ new_instance[0].id, instance_ip ]

