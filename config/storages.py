import environ
from storages.backends.s3boto3 import S3Boto3Storage

env = environ.Env()
bucket = env.str('DJANGO_S3_BUCKET_NAME', None)


class _Storage(S3Boto3Storage):
    bucket_name = bucket
    custom_domain = f'{bucket}.fra1.digitaloceanspaces.com'


class StaticStorage(S3Boto3Storage):
    location = 'static'


class MediaStorage(S3Boto3Storage):
    location = 'uploads'
