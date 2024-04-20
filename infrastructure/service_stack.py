from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda,
    aws_sqs as sqs,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct


class ServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        PythonFunction(
            self,
            "LambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            entry="./app/lambdas",
            index="example2.py",
            handler="lambda_handler",
        )
