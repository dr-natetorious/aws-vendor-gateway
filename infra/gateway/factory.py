from infra.gateway.networking import GatewayNetworking
from aws_cdk.core import Construct

class GatewayFactory(Construct):

  def __init__(self, scope: Construct, id: str, cidr:str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.networking = GatewayNetworking(self,'Networking',cidr=cidr)