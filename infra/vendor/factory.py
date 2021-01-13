from infra.vendor.apps import AppConstruct
from infra.vendor.networking import VendorNetworking
from infra.shared.vpce import VpcEndpointsForIsolatedSubnets

from aws_cdk.core import Construct

class VendorFactory(Construct):

  def __init__(self, scope: Construct, id: str, cidr:str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.networking = VendorNetworking(self,'Networking',cidr=cidr)
    VpcEndpointsForIsolatedSubnets(self,'VPC-e',vpc=self.networking.vpc)
    AppConstruct(self,'AppTier',vpc=self.networking.vpc)