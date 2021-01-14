#!/usr/bin/env python2
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class VpcSubnetBinder(core.Construct):
  """
  Configure and deploy the network
  """
  def __init__(self, scope: core.Construct, id: str, vpc:ec2.IVpc,subnets:ec2.SubnetSelection, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)
