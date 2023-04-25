import boto3
import uuid
import os

import config

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
