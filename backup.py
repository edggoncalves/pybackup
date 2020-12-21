import boto3
from api_request import request
from configure import configuration


def _build_target(settings, key) -> str:
    api = settings.get('api').get('address', 'https://api.linode.com/v4')
    endpoint = settings.get('api').get('buckets_endpoint', '')
    cluster = request('/'.join((api, endpoint)), key).get('data')[0].get('cluster')
    target = '/'.join([
        api,
        endpoint,
        cluster
    ])

    return target


def _s3_client(buckets_info, access_key, secret_key):
    hostname = buckets_info.get('data', {})[0].get('hostname', '')
    endpoint_url = 'https://{}'.format('.'.join(hostname.split('.')[1:]))
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
    )
    return client


def do_something():
    settings, token, access_key, secret_key = configuration()
    target = _build_target(settings, token)
    buckets_info = request(target, token)
    client = _s3_client(buckets_info, access_key, secret_key)
    list_buckets = client.list_buckets().get('Buckets')
    if len(list_buckets) == 1:
        bucket = list_buckets[0]
        contents = client.list_objects_v2(Bucket=bucket.get('Name'))

        print(contents.get('Contents'))


do_something()
