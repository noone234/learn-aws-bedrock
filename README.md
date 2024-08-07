# sumaud

I'm learning AWS Bedrock, and writing code along the way.

This project uses AWS's Cloud Development Kit (CDK).
CDK provided much of the following documentation.

# First project: SumAud

Given an audio recording of a conversation,
transcribe and summarize that conversation.
That is the goal of this project.

# Supported audio formats

This project accepts a variety of audio formats as input.

Recommended formats:

- FLAC
- WAV with PCM 16-bit encoding

Supported formats:

- AMR
- FLAC
- M4A
- MP3
- MP4
- Ogg
- WebM
- WAV

# Requirements

- Python 3.12
- AWS CLI
- AWS Cloud Development Kit (CDK)
- AWS account that you can deploy this project to. You or your company should own this AWS account.

# Usage

## Setup

1. Create a local clone of this GitHub repo.
2. Create a Python virtual environment that uses Python 3.12.
3. Activate the Python virtual environment.
4. Install requirements.

Here are sample commands.

```
python -m venv env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Installation

Assuming that you have valid AWS credentials, run:

`cdk deploy`

## Testing

Log into AWS Management Console.
Enter the AWS account that you just deployed this project to.

In the S3 bucket that this service created, upload a recording of a
conversation to the `audio` folder.  Confirm that the file uses a
supported audio format.

This should result in a:

- full `transcript`, in the S3 bucket's `transcripts` folder
- text summary, in a file named `results.txt`

## Notes

This is a Proof of Concept (POC).

It is also a working example.

When I started my learning journey,
I was presented with notebooks that contained partial, outdated source code.
Copying and pasting that code to try it out resulted in errors. Nothing worked.
Building a complete functional project helped me learn.

This can be done with AWS Step Functions instead of Lambda functions. I hestitated to go that far in a first project.  It would be teaching one more AWS technology.  It is already
a stretch for software engineers to learn the technologies involved so far.  Adding 1 more, especially for engineers who have not yet embraced Step Functions, would be too much of a learning curve.

# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
