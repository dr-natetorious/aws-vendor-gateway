from infra.vendor.factory import VendorFactory
from aws_cdk.core import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class VendorPrivateLink(Construct):
  def __init__(self, scope: Construct, id: str, vendor:VendorFactory,gateway_vpc:ec2.IVpc, subnets:ec2.SubnetSelection, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.security_group = ec2.SecurityGroup(self,'VendorPL',
      vpc=gateway_vpc,
      allow_all_outbound=True,
      description='Group for accessing {} private link'.format(id))

    # ec2.InterfaceVpcEndpoint(self,id,
    #   vpc=gateway_vpc,
    #   service= vendor.endpoints.apache_cluster,
    #   open=True,
    #   private_dns_enabled=False,
    #   lookup_supported_azs=False,
    #   security_groups=[self.security_group],
    #   subnets=subnets)
