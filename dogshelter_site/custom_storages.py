from storages.backends.s3boto3 import S3Boto3Storage


# Media Storage class for storing media files in the S3 bucket
class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
