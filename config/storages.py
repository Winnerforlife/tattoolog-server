import environ
from storages.backends.s3boto3 import S3Boto3Storage

env = environ.Env()
bucket = env.str('DJANGO_S3_BUCKET_NAME', None)
print(f"storages | bucket - {bucket}")


class _Storage(S3Boto3Storage):
    bucket_name = bucket
    custom_domain = f'{bucket}.fra1.digitaloceanspaces.com'


class StaticStorage(_Storage):
    location = 'static'


class MediaStorage(_Storage):
    location = 'uploads'
