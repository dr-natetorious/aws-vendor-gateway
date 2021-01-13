#!/usr/bin/env python3
import os.path
from aws_cdk.core import App, Stack, Environment
from infra.networking import BaseNetworkingLayer
from infra.vendor import VendorConstruct
src_root_dir = os.path.join(os.path.dirname(__file__))

default_env= Environment(region="us-west-2")

def create_infra_stack(infra_stack):
  networking = BaseNetworkingLayer(infra_stack,'Networking')
  vendor_a = VendorConstruct(infra_stack,'VendorA',vpc=networking.vendor_a_vpc)
  #vendor_b = VendorConstruct(infra_stack,'VendorB',vpc=networking.vendor_b_vpc)
  

app = App()
infra_stack = Stack(app,'VndrGtwy', env=default_env)
create_infra_stack(infra_stack)

app.synth()
