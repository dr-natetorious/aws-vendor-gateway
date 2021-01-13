from infra.vendor.apps import AppConstruct
from infra.vendor.networking import VendorNetworking
from infra.shared.ssm import SystemsManagerEndpoints

from aws_cdk.core import Construct

class VendorFactory(Construct):

  def __init__(self, scope: Construct, id: str, cidr:str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.networking = VendorNetworking(self,'Networking',cidr=cidr)
    SystemsManagerEndpoints(self,'SysMgr',vpc=self.networking.vpc)