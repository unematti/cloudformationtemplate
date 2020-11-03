import boto3, time


ec2 = boto3.client('ec2')
cf = boto3.client('cloudformation')

cf.create_stack(StackName='something', TemplateURL='https://templates-cmdrunematti.s3.eu-central-1.amazonaws.com/templates/cloudformation.yaml')
ec2.create_security_group(Description='test', GroupName='testsecuritygroup')

