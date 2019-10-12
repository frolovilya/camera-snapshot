import boto3
import boto3.exceptions

import logger


class S3Exception(Exception):
    def __init__(self, message, s3_exception):
        self.message = message + str(s3_exception)


class S3Client:
    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        self._bucket_name = bucket_name
        self._s3 = boto3.client('s3',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key)

    def upload(self, source_file_path: str, target_file_path: str):
        """
        Upload source_file_path to Amazon S3 storage at bucket_name/target_file_path.
        """
        try:
            logger.log("Uploading {} to S3 {}/{}...", source_file_path, self._bucket_name, target_file_path)
            self._s3.upload_file(source_file_path, self._bucket_name, target_file_path)
            logger.log("Uploaded {}/{}", self._bucket_name, target_file_path)
        except boto3.exceptions.Boto3Error as e:
            raise S3Exception("Error uploading file to S3: ", e)
