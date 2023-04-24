import boto3
import uuid
import os

import config
from botocore.client import Config


def upload_file_to_s3(file_path, content_type):
    """
    Upload a file to an S3 bucket

    :param file_path: Path to the file to upload
    :param bucket_name: Name of the bucket to upload to
    :param object_name: Object name to use for the uploaded file
    :param access_key: Access key for the S3 client
    :param secret_key: Secret key for the S3 client
    :return: True if the file was uploaded, else False
    """

    # Create an S3 client with access key and secret key
    s3 = boto3.client(
        "s3",
        endpoint_url=config.AWS_S3_BASE_URL,
        aws_access_key_id=config.AWS_S3_ACCESS_KEY,
        aws_secret_access_key=config.AWS_S3_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'  # Default Minio region
    )

    # Upload the file
    try:
        response = s3.upload_file(
            file_path.split("/")[-1],
            config.AWS_S3_BUCKET,
            file_path,
            ExtraArgs={"ACL": "public-read", "ContentType": content_type},
        )
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

    print(f"{file_path} uploaded to {config.AWS_S3_BUCKET}/{file_path}")
    return True


def get_uuid():
    return str(uuid.uuid4())


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
        return True
    else:
        print(f"{file_path} does not exist.")
        return False
