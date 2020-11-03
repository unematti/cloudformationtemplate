import boto3
import time

cf = boto3.client('cloudformation')
s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

securitygroups = ec2.describe_security_groups()
instances = ec2.describe_instances()
cfresponse = cf.describe_stacks()


for stack in cfresponse['Stacks']:
    print('for1', stack['StackStatus'])
    if 'RootId' not in stack and stack['StackStatus'] == 'CREATE_COMPLETE':
        print('if1',stack['StackName'])
        cf.delete_stack(StackName = stack['StackName'])
        while True: 
            try: 
                thing = cf.describe_stack_events(StackName = stack['StackName'])
            except:
                break
            print('waiting')
            time.sleep(15)
        print('deletion of stack', stack['StackName'], 'is complete')

for reservation in instances["Reservations"]: #checks for remaining instances in ec2
    for instance in reservation["Instances"]:
        if instance['State']['Name'] != 'terminated': 
            ec2.terminate_instances(InstanceIds = [instance['InstanceId']]) #terminates remaining instances
            print('instance', instance['InstanceId'], 'has been terminated')
            time.sleep(5)

for group in securitygroups['SecurityGroups']: #looks for remaining security groups
    print(group['GroupId'])
    try:
        ec2.delete_security_group(GroupId = group['GroupId']) #deletes if theres any
        print('the ', group['GroupId'], ' group has been removed')        
    except:
        print('the group couldnt be deleted')


for bucket in s3.buckets.all():
    print(bucket.name)
