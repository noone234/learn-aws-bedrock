import boto3
import json

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

prompt = "Write a one sentence summary of Las Vegas."

kwargs = {
    "modelId": "amazon.titan-text-lite-v1",
    "contentType": "application/json",
    "accept": "*/*",
    "body": json.dumps({"inputText": prompt}),
}

response = bedrock_client.invoke_model(**kwargs)
response_body = json.loads(response["body"].read())

print(json.dumps(response_body, indent=2))
print(response_body["results"][0]["outputText"])
