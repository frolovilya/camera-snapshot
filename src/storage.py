import boto3
import boto3.exceptions

import logger


class StorageException(Exception):
    def __init__(self, message, s3_exception):
        self.message = message + str(s3_exception)


class S3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        self.bucket_name = bucket_name
        self.__s3 = boto3.client('s3',
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)

    def upload(self, source_file_path, target_file_path):
        try:
            logger.log("Uploading {} to S3 {}/{}...", source_file_path, self.bucket_name, target_file_path)
            self.__s3.upload_file(source_file_path, self.bucket_name, target_file_path)
            logger.log("Uploaded {}/{}", self.bucket_name, target_file_path)
        except boto3.exceptions.Boto3Error as e:
            raise StorageException("Error uploading file to S3: ", e)
