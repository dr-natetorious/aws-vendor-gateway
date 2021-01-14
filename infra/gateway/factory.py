from infra.vendor.factory import VendorFactory
from infra.gateway.networking import GatewayNetworking
from infra.gateway.vendorlink import VendorPrivateLink
from aws_cdk.core import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class GatewayFactory(Construct):

  def __init__(self, scope: Construct, id: str, cidr:str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)
    self.networking = GatewayNetworking(self,'Networking',cidr=cidr)

  def bind_vendor(self, id, vendor:VendorFactory,subnets:ec2.SubnetSelection) -> VendorPrivateLink:
    return VendorPrivateLink(
      scope=self,
      id= id,
      vendor=vendor,
      gateway_vpc=self.networking.vpc,
      subnets=subnets)

