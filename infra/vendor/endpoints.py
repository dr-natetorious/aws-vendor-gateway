from aws_cdk import (
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_elasticloadbalancingv2 as elb,
  aws_elasticloadbalancingv2_targets as t,
  core
)

class VendorEndpoints(core.Construct):

  def __init__(self, scope: core.Construct, id: str, nlb:ec2.IVpcEndpointServiceLoadBalancer, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    self.apache_cluster = ec2.VpcEndpointService(self,'ApacheNLB',
      vpc_endpoint_service_load_balancers=[nlb],
      acceptance_required=False,
      whitelisted_principals=[iam.ArnPrincipal(arn='*')])