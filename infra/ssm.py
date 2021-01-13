from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_elasticloadbalancingv2 as elb,
  aws_elasticloadbalancingv2_targets as t,
  core
)

class SystemsManagerConstruct(core.Construct):
  """
  Configure the Vendor Application
  """
  def __init__(self, scope: core.Construct, id: str, vpc:ec2.IVpc, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.security_group = ec2.SecurityGroup(self,'SSM-EndpointSecurity',
      vpc=vpc,
      allow_all_outbound=True,
      description='SG for SSM Vpc Endpoints')

    self.security_group.add_ingress_rule(
      peer= ec2.Peer.any_ipv4(),
      connection=ec2.Port(
        protocol= ec2.Protocol.ALL,
        string_representation='Any source'))

    self.gateways = {}
    for svc in ['s3']:
      self.gateways[svc] = ec2.GatewayVpcEndpoint(self,'VPCe-'+svc,
      vpc=vpc,
      service= ec2.GatewayVpcEndpointAwsService(
        name=svc))

    self.interfaces = {}
    for svc in ['ssm','ec2messages','ec2','ssmmessages','kms']:
      self.interfaces[svc] = ec2.InterfaceVpcEndpoint(self,'VPCe-'+svc,
      vpc=vpc,
      service= ec2.InterfaceVpcEndpointAwsService(
        name=svc),
      open=True,
      private_dns_enabled=True,
      lookup_supported_azs=False,
      security_groups=[self.security_group])
