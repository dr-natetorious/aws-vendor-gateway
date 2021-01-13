#!/usr/bin/env python3
import os.path
from aws_cdk.core import App, Stack, Environment
from infra.vendor.factory import VendorFactory
src_root_dir = os.path.join(os.path.dirname(__file__))

default_env= Environment(region="us-west-2")

def create_infra_stack(infra_stack):
  VendorFactory(infra_stack,'VendorA',cidr='10.10.0.0/16')

app = App()
infra_stack = Stack(app,'VndrGtwy', env=default_env)
create_infra_stack(infra_stack)

app.synth()
