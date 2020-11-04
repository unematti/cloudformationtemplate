import time
import boto3

s3 = boto3.resource('s3')



print('\033[91m' + 'Deleting Stacks' + '\033[0m')

cf = boto3.client('cloudformation')
cfresponse = cf.describe_stacks()
stackwaiter = cf.get_waiter('stack_delete_complete')
for stack in cfresponse['Stacks']:
    if 'RootId' not in stack and stack['StackStatus'] == 'CREATE_COMPLETE':
        print('Deletin stack', stack['StackName'], 'is complete')
        cf.delete_stack(StackName = stack['StackName'])
        stackwaiter.wait(StackName = stack['StackName'])
        print('Deletion of stack', stack['StackName'], 'is complete')

print('\033[91m' + 'Deleting remainder Loadbalancers' + '\033[0m')

lb = boto3.client('elb')
lbresponse = lb.describe_load_balancers()
loadbalancerwaiter = lb.get_waiter('any_instance_in_service')
for loadbalancer in lbresponse['LoadBalancerDescriptions']:
    print('Deleting ', loadbalancer['LoadBalancerName'])
    lb.delete_load_balancer(LoadBalancerName = loadbalancer['LoadBalancerName'])
    loadbalancerwaiter.wait(LoadBalancerName = loadbalancer['LoadBalancerName'])
    print('Deletiion of loadbalancer ', loadbalancer['LoadBalancerName'], 'is complete')

print('\033[91m' + 'Deleting remainder AutoScaling Groups' + '\033[0m')

asg = boto3.client('autoscaling')
asgresponse = asg.describe_auto_scaling_groups()
lcresponse = asg.describe_launch_configurations()
for asgroup in asgresponse['AutoScalingGroups']:
    print('Deleting ', asgroup['AutoScalingGroupName'])
    try:
        asg.delete_auto_scaling_group(AutoScalingGroupName = asgroup['AutoScalingGroupName'], ForceDelete=True)
        print(asgroup['AutoScalingGroupName'], ' is deleted')
    except:
        print(asgroup['AutoScalingGroupName'], ' couldnt be deleted')
for lc in lcresponse['LaunchConfigurations']:
    print('Deleting ', lc['LaunchConfigurationName'])
    try:
        asg.delete_launch_configuration(LaunchConfigurationName = lc['LaunchConfigurationName'])
        print(lc['LaunchConfigurationName'], ' is deleted')
    except:
        print(lc['LaunchConfigurationName'], ' couldnt be deleted')




print('\033[91m' + 'Deleting remainder Instances' + '\033[0m')

ec2 = boto3.client('ec2')
instances = ec2.describe_instances()
instancewaiter = ec2.get_waiter('instance_terminated')
for reservation in instances["Reservations"]: #checks for remaining instances in ec2
    for instance in reservation["Instances"]:
        if instance['State']['Name'] != 'terminated':
            print('Deleting ', instance['InstanceId'])
            ec2.terminate_instances(InstanceIds = [instance['InstanceId']]) #terminates remaining instances
            instancewaiter.wait(InstanceIds = [instance['InstanceId']])
            print('instance', instance['InstanceId'], 'has been terminated')
            time.sleep(5)

print('\033[91m' + 'Deleting remainder Security Groups' + '\033[0m')

securitygroups = ec2.describe_security_groups()
for group in securitygroups['SecurityGroups']: #looks for remaining security groups
    print('Deleting ', group['GroupId'])
    try:
        ec2.delete_security_group(GroupId = group['GroupId']) #deletes if theres any
        print('the ', group['GroupId'], ' group has been removed')
    except:
        print('the group couldnt be deleted')


#for bucket in s3.buckets.all():
#    print(bucket.name)
