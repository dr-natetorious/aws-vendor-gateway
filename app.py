#!/usr/bin/env python3
import os.path
from aws_cdk.core import App, Stack, Environment
from infra.vendor.factory import VendorFactory
from infra.gateway.factory import GatewayFactory
src_root_dir = os.path.join(os.path.dirname(__file__))

default_env= Environment(region="us-west-2")

def create_infra_stack(infra_stack):
  VendorFactory(infra_stack,'VendorA',cidr='10.10.0.0/16')
  #GatewayFactory(infra_stack,'Gateway',cidr='10.30.0.0/16')

app = App()
infra_stack = Stack(app,'VndrGtwy', env=default_env)
create_infra_stack(infra_stack)

app.synth()
