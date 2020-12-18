import yaml
import urllib3
import json
import boto3


def _configuration():
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.load(stream, Loader=yaml.SafeLoader).get('buckets_settings', {})
            token = settings.get('api').get('key', '')
            access_key = settings.get('bucket_keys').get('access_key', '')
            secret_key = settings.get('bucket_keys').get('secret_key', '')
            return settings, token, access_key, secret_key
        except yaml.YAMLError as exception:
            print(exception)


def _request(target, token):
    http = urllib3.PoolManager()
    headers = {
                'Authorization': 'Bearer {}'.format(token),
                'Content-type': 'application/json'
            }

    r = http.request(
            method='GET',
            url=target,
            headers=headers,
            timeout=10.0,
    )
    r = r.data.decode('utf8')
    r = json.loads(r)

    return r


def _build_target(settings, key):
    api = settings.get('api').get('address', 'https://api.linode.com/v4')
    endpoint = settings.get('api').get('buckets_endpoint', '')
    cluster = _request('/'.join((api, endpoint)), key).get('data')[0].get('cluster')
    target = '/'.join([
        api,
        endpoint,
        cluster
    ])

    return target


def _list_buckets(buckets_info, token, access_key, secret_key):
    hostname = buckets_info.get('data', {})[0].get('hostname', '')
    endpoint_url = 'https://{}'.format('.'.join(hostname.split('.')[1:]))
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
    )

    buckets = client.list_buckets().get('Buckets')

    return buckets


def do_something():
    settings, token, access_key, secret_key = _configuration()
    target = _build_target(settings, token)
    buckets_info = _request(target, token)
    list_buckets = _list_buckets(buckets_info, token, access_key, secret_key)

    print(list_buckets)


do_something()
