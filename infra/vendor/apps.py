import os.path
from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_elasticloadbalancingv2 as elb,
  aws_elasticloadbalancingv2_targets as t,
  core
)

# Cache the machine start-up script
user_data = None
src_root_dir = os.path.dirname(__file__)
with open(os.path.join(src_root_dir,'./user_data.sh'),'r') as file:
  user_data = file.read()

class AppConstruct(core.Construct):
  """
  Configure the Vendor Application
  """
  def __init__(self, scope: core.Construct, id: str, vpc:ec2.IVpc, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)
    
    self.security_group = ec2.SecurityGroup(self,'{}-Instances'.format(id),
      vpc=vpc,
      allow_all_outbound=True,
      description='Instances within {} VPC'.format(id))    
    
    # Create the EC2 Instances
    machine_image = ec2.MachineImage().generic_linux(
      ami_map={'us-west-2':'ami-0a61cc598d5d50aa8'},
      user_data= ec2.UserData.for_linux(shebang=user_data))

    count=0
    instances = []
    for subnet in vpc.select_subnets(subnet_group_name='Services').subnets:
      count+=1

      # Create the object
      instance = ec2.Instance(self, '{}-Instance-{}'.format(id,count),
        instance_type=ec2.InstanceType('t2.micro'),
        vpc=vpc,
        allow_all_outbound=True,
        machine_image=machine_image,
        vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
        security_group=self.security_group,
        user_data_causes_replacement=True)
      
      instance.role.add_managed_policy(
        policy= iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
      instances.append(t.InstanceTarget(instance=instance, port=80))

    # Create the load balancer
    self.load_balancer = elb.ApplicationLoadBalancer(self,'LoadBalancer',
      vpc=vpc,
      deletion_protection=False,
      ip_address_type= elb.IpAddressType.IPV4,
      security_group=self.security_group,
      internet_facing=False,
      vpc_subnets= ec2.SubnetSelection(subnet_group_name='Services'))

    self.target_group = elb.ApplicationTargetGroup(self,'TargetGroup',
      port=80,
      vpc=vpc,
      protocol=elb.ApplicationProtocol.HTTP,
      targets= instances,
      health_check=elb.HealthCheck(
        enabled=True,
        path='/'))

    self.listener = elb.ApplicationListener(self,'Listener',
      load_balancer=self.load_balancer,
      default_action= elb.ListenerAction.forward(
        target_groups=[self.target_group]),
      protocol= elb.Protocol.HTTP,
      port=80)
