import boto3
import time

cf = boto3.client('cloudformation')
s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

instancewaiter = ec2.get_waiter('instance_terminated')
stackwaiter = cf.get_waiter('stack_delete_complete')
securitygroups = ec2.describe_security_groups()
instances = ec2.describe_instances()
cfresponse = cf.describe_stacks()


print('\033[91m' + 'Deleting Stacks' + '\033[0m')

for stack in cfresponse['Stacks']:
    print('Deleting ' ,stack['StackName'])
    if 'RootId' not in stack and stack['StackStatus'] == 'CREATE_COMPLETE':
        cf.delete_stack(StackName = stack['StackName'])
        stackwaiter.wait(StackName = stack['StackName'])
        print('deletion of stack', stack['StackName'], 'is complete')

print('\033[91m' + 'Deleting remainder Instances' + '\033[0m')

for reservation in instances["Reservations"]: #checks for remaining instances in ec2
    for instance in reservation["Instances"]:
        if instance['State']['Name'] != 'terminated': 
            print('Deleting ', instance['InstanceId'])
            ec2.terminate_instances(InstanceIds = [instance['InstanceId']]) #terminates remaining instances
            instancewaiter.wait(InstanceIds = [instance['InstanceId']])
            print('instance', instance['InstanceId'], 'has been terminated')
            time.sleep(5)

print('\033[91m' + 'Deleting remainder Security Groups' + '\033[0m')

for group in securitygroups['SecurityGroups']: #looks for remaining security groups
    print(group['GroupId'])
    try:
        ec2.delete_security_group(GroupId = group['GroupId']) #deletes if theres any
        print('the ', group['GroupId'], ' group has been removed')        
    except:
        print('the group couldnt be deleted')


#for bucket in s3.buckets.all():
#    print(bucket.name)
