#!/usr/bin/env python2
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class VendorNetworking(core.Construct):
  """
  Configure and deploy the network
  """
  def __init__(self, scope: core.Construct, id: str, cidr:str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.__vpc = ec2.Vpc(self,'Vpc', cidr=cidr,
      enable_dns_hostnames=True,
      enable_dns_support=True,
      max_azs=3,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='Services',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])

  @property
  def vpc(self) -> ec2.Vpc:
    return self.__vpc