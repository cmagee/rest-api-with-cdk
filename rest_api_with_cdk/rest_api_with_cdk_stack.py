from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_apigateway as _api,
)


class RestApiWithCdkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        function = _lambda.Function(
            self,
            "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset("src"),
            handler="handler.lambda_handler",
            function_name="rest-api-lambda",
            timeout=core.Duration.seconds(60),
            environment={  # Simple way of setting env vars for you function
                "FOO": "BAR"
            },
        )

        # define the API gateway resource
        api = _api.LambdaRestApi(
            self,
            "MyLambdaRestApi",
            handler=function,
            proxy=False,
            deploy_options={  # Defaults to a production deployment without this
                "logging_level": _api.MethodLoggingLevel.INFO,
                "stage_name": "dev",
            },
            endpoint_configuration={
                "types": [
                    _api.EndpointType.REGIONAL
                ]  # Learn more about the various endpoint types here: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-endpoint-types.html
            },
        )

        # Now add resources and methods to the API
        v1 = api.root.add_resource("v1")
        health_check = v1.add_resource("healthcheck")
        health_check_method = health_check.add_method(
            "GET", api_key_required=True
        )  # GET /v1/healthcheck

        # Below will generate an API key for this API
        plan = api.add_usage_plan(
            "MyAPIUsagePlan",
            name="Default",
            throttle={"rate_limit": 500, "burst_limit": 100},
        )

        plan.add_api_stage(
            stage=api.deployment_stage,
            throttle=[
                {
                    "method": health_check_method,
                    "throttle": {"rate_limit": 500, "burst_limit": 100},
                }
            ],
        )
        api_key = api.add_api_key("APIKey")
        plan.add_api_key(
            api_key
        )  # Grab the API Key from the API Gateway console: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html
