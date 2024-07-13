import logging
import uuid
import os

import boto3

s3_client = boto3.client("s3")
transcribe_client = boto3.client("transcribe")


def lambda_handler(event, context):
    # Extract bucket and file name from incoming event.
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    # Infer audio format from input file extension.
    audio_format = key.split(".")[-1]

    job_name = "transcription-job-" + str(uuid.uuid4())  # Needs to be a unique name

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{bucket}/{key}"},
        MediaFormat=audio_format,
        LanguageCode="en-US",
        OutputBucketName=os.environ["S3_BUCKET_NAME"],
        OutputKey=f"{os.environ['S3_TRANSCRIPT_PATH']}{job_name}-transcript.json",
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 2},
    )

    logging.info(f"Submitted transcription job for {key} from bucket {bucket}.")
