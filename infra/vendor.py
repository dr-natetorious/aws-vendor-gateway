from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_elasticloadbalancingv2 as elb,
  aws_elasticloadbalancingv2_targets as t,
  core
)

class VendorConstruct(core.Construct):
  """
  Configure and deploy the network
  """
  def __init__(self, scope: core.Construct, id: str, vpc:ec2.IVpc, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)
    
    machine_image = ec2.MachineImage().generic_linux(
        ami_map={'us-west-2':'ami-0a36eb8fadc976275'},
        user_data= ec2.UserData.for_linux(shebang="""
        # Install Apache
        yum -y install httpd
        service httpd start
        echo "<html><h1>hello from `hostname`</h1></html>" > /var/www/html/index.html

        # Install SSM
        yum install -y https://s3.us-west-2.amazonaws.com/amazon-ssm-us-west-2/latest/linux_amd64/amazon-ssm-agent.rpm
        """)
    )

    self.security_group = ec2.SecurityGroup(self,'{}-Instances'.format(id),
      vpc=vpc,
      allow_all_outbound=True,
      description='Instances within {} VPC'.format(id))    

    self.load_balancer = elb.ApplicationLoadBalancer(self,'LoadBalancer',
      vpc=vpc,
      deletion_protection=False,
      ip_address_type= elb.IpAddressType.IPV4,
      security_group=self.security_group,
      internet_facing=False,
      vpc_subnets= ec2.SubnetSelection(subnet_group_name='Services'))

    # Create the EC2 Instances
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

    # Create the target group
    self.target_group = elb.ApplicationTargetGroup(self,'TargetGroup',
      port=80,
      vpc=vpc,
      protocol=elb.ApplicationProtocol.HTTP,
      targets= instances,
      health_check=elb.HealthCheck(
        enabled=True,
        path='/index.html'))

    self.listener = elb.ApplicationListener(self,'Listener',
      load_balancer=self.load_balancer,
      default_action= elb.ListenerAction.forward(
        target_groups=[self.target_group]),
      protocol= elb.Protocol.HTTP,
      port=80)
