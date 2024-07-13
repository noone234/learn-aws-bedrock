from aws_cdk import (
    # Duration,
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_sqs as sqs,
    aws_s3 as s3,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct


class ServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "Schaiver",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        lambdaTranscriber = PythonFunction(
            self,
            "Transcriber",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            entry="./app/lambdas",
            index="transcribe.py",
            handler="lambda_handler",
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name,
                "S3_AUDIO_PATH": "audio/",
                "S3_TRANSCRIPT_PATH": "transcript/",
            },
        )
        transcription_policy = iam.PolicyStatement(
            actions=["transcribe:StartTranscriptionJob"],
            resources=["*"],
            effect=iam.Effect.ALLOW,
        )
        lambdaTranscriber.add_to_role_policy(transcription_policy)

        lambdaSummarizer = PythonFunction(
            self,
            "Summarizer",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            entry="./app/lambdas",
            index="summarize.py",
            handler="lambda_handler",
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name,
                "S3_TRANSCRIPT_PATH": "transcript/",
                "S3_SUMMARY_PATH": "summary/",
            },
        )
        summarization_policy = iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=[
                "arn:aws:bedrock:*::foundation-model/amazon.titan-text-express-v1"
            ],
            effect=iam.Effect.ALLOW,
        )
        lambdaSummarizer.add_to_role_policy(summarization_policy)

        # Trigger a Lambda function when an audio file is uploaded to an S3 bucket.
        s3PutEventSource = lambda_event_sources.S3EventSource(
            bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(prefix="audio/")],
        )
        lambdaTranscriber.add_event_source(s3PutEventSource)
        bucket.grant_read_write(lambdaTranscriber)

        # Trigger a Lambda function when a transcript file is uploaded to an S3 bucket.
        s3PutEventSource = lambda_event_sources.S3EventSource(
            bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(prefix="transcript/")],
        )
        lambdaSummarizer.add_event_source(s3PutEventSource)
        bucket.grant_read_write(lambdaSummarizer)
