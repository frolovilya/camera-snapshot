import boto3
from src import logger


class S3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        self.bucket_name = bucket_name
        self.__s3 = boto3.client('s3',
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)

    def upload(self, source_file_path, target_file_path):
        logger.log("Uploading {} to S3 {}...", source_file_path, target_file_path)
        self.__s3.upload_file(source_file_path, self.bucket_name, target_file_path)
        logger.log("Uploaded {}", target_file_path)