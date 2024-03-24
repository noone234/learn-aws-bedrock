import aws_cdk as core
import aws_cdk.assertions as assertions

from learn_aws_bedrock.learn_aws_bedrock_stack import LearnAwsBedrockStack

# example tests. To run these tests, uncomment this file along with the example
# resource in learn_aws_bedrock/learn_aws_bedrock_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LearnAwsBedrockStack(app, "learn-aws-bedrock")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
