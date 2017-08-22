import boto3

class aws ( object, ):
    def __init__( self, region ):
        self.region = region
        self.ec2_resource = boto3.resource( 'ec2', self.region )
        self.ec2_client = boto3.client ( 'ec2', self.region)
        self.ec2_waiter = self.ec2_client.get_waiter('instance_status_ok')

    def create_tag ( self, ec2_object, key, value ):
        tags = ec2_object.create_tags(
           Tags=[
                {
                  'Key': key,
                  'Value': value
                }

            ]
        )
        return tags