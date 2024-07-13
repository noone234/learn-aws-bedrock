import boto3
import json
import logging

bedrock_client = boto3.client("bedrock-runtime")
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    # One of a few different checks to ensure we don't end up in a recursive loop.
    if "-transcript.json" not in key:
        logging.warning("This demo only works with *-transcript.json.")
        return

    file_content = ""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    file_content = response["Body"].read().decode("utf-8")

    transcript = extract_transcript_from_textract(file_content)

    logging.info(f"Successfully read file {key} from bucket {bucket}.")
    logging.info(f"Transcript: {transcript}")

    summary = bedrock_summarisation(transcript)

    output_key = key.replace("-transcript.json", "-summary.txt")
    s3_client.put_object(
        Bucket=bucket, Key="results.txt", Body=summary, ContentType="text/plain"
    )

    logging.info(
        f"Successfully summarized {key} from bucket {bucket}. Summary: {output_key}"
    ),


def extract_transcript_from_textract(file_content):
    transcript_json = json.loads(file_content)

    output_text = ""
    current_speaker = None

    items = transcript_json["results"]["items"]

    # Iterate through the content word by word:
    for item in items:
        speaker_label = item.get("speaker_label", None)
        content = item["alternatives"][0]["content"]

        # Start the line with the speaker label:
        if speaker_label is not None and speaker_label != current_speaker:
            current_speaker = speaker_label
            output_text += f"\n{current_speaker}: "

        # Add the speech content:
        if item["type"] == "punctuation":
            output_text = output_text.rstrip()  # Remove the last space

        output_text += f"{content} "

    return output_text


def bedrock_summarisation(transcript_text: str):
    prompt = f"""The text between the <transcript> XML tags is a transcript of a conversation. 
    Write a short summary of the conversation.

    <transcript>
    {transcript_text}
    </transcript>

    Here is a summary of the conversation in the transcript:"""
    print(prompt)

    kwargs = {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2048,
                    "stopSequences": [],
                    "temperature": 0,
                    "topP": 0.9,
                },
            }
        ),
    }

    response = bedrock_client.invoke_model(**kwargs)

    summary = (
        json.loads(response.get("body").read()).get("results")[0].get("outputText")
    )
    return summary
