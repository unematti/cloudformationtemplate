from random import randint as randint
import boto3


ec2 = boto3.client('ec2')
response = ec2.describe_instances(Filters = [{'Name' : 'instance-state-name', 'Values' : ['running'] }])
waiter = ec2.get_waiter('instance_terminated')

lenght = len(response['Reservations'])
if not lenght: 
    exit('There are no instances to terminate')
choose = randint( 0, lenght)

instance = (response['Reservations'][choose]['Instances'][0]['InstanceId'])
print('Terminating instance:', instance, 'out of', lenght, 'instances' )
ec2.terminate_instances(InstanceIds = [instance])
waiter.wait(InstanceIds = [instance])
print('done')
