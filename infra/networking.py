#!/usr/bin/env python2
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class BaseNetworkingLayer(core.Construct):
  """
  Configure and deploy the network
  """
  def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    # Create Vendors...
    self.vendor_a_vpc = ec2.Vpc(self,'VendorA', cidr='10.10.0.0/16',
      enable_dns_hostnames=True,
      enable_dns_support=True,
      max_azs=3,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='Services',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])
    
    self.vendor_b_vpc = ec2.Vpc(self,'VendorB', cidr='10.20.0.0/16',
      enable_dns_hostnames=True,
      enable_dns_support=True,
      max_azs=3,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='Services',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])

    # Create the apps...
    self.app_a_vpc = ec2.Vpc(self,'AppC', cidr='10.20.0.0/16',
      enable_dns_hostnames=True,
      enable_dns_support=True,
      nat_gateways=1,
      max_azs=3,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='WebPortal',subnet_type= ec2.SubnetType.PUBLIC, cidr_mask=24),
        ec2.SubnetConfiguration(name='Services',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])

    self.app_b_vpc = ec2.Vpc(self,'AppD', cidr='10.40.0.0/16',
      enable_dns_hostnames=True,
      enable_dns_support=True,
      nat_gateways=1,
      max_azs=3,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='WebPortal',subnet_type= ec2.SubnetType.PUBLIC, cidr_mask=24),
        ec2.SubnetConfiguration(name='Services',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])

    self.vendor_gateway = ec2.Vpc(self,'VendorGateway', cidr='10.50.0.0/16',enable_dns_hostnames=True,
      enable_dns_support=True,
      nat_gateways=0,
      max_azs=2,
      subnet_configuration= [
        ec2.SubnetConfiguration(name='VendorA',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
        ec2.SubnetConfiguration(name='VendorB',subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
      ])
