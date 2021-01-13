# aws-vendor-gateway

Example for brokering multiple vendors into a dedicated connection account

## Setup instructions

1. Create a test account
2. This example uses 5 VPC -- you either need to delete the default VPC in a region or request capacity increase
3. Build the deployment image `docker build -t cdk-deploy ./images/cdk-deploy`
4. Launch the build container `docker run -v %user_profile%\.aws:/root/.aws -v .:/files -w /files cdk-deploy`
5. Invoke `ship-it`
