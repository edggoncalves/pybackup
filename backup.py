import yaml
import urllib3
import json


def _configuration():
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.load(stream, Loader=yaml.SafeLoader).get('buckets_settings', {})
            return settings
        except yaml.YAMLError as exception:
            print(exception)


def _request(target, key):
    http = urllib3.PoolManager()
    headers = {
                'Authorization': 'Bearer {}'.format(key),
                'Content-type': 'application/json'
            }

    r = json.loads(
        http.request(
            method='GET',
            url=target,
            headers=headers,
            timeout=10.0,
        ).data.decode('utf8')
    )

    return print(r.get('data')[0])


def _build_args(settings):
    api = settings.get('api').get('address', 'https://api.linode.com/v4')
    endpoint = settings.get('api').get('buckets_endpoint', '')
    cluster_id = settings.get('backup_bucket').get('cluster', '')
    args = [api, endpoint, cluster_id]
    target = '/'.join([arg for arg in (args or [])])

    return target


def do_something():
    settings = _configuration()
    target = _build_args(settings)
    key = settings.get('api').get('key', '')

    _request(target, key)


do_something()
