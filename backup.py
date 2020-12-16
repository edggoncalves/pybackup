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


def do_something():
    settings = _configuration()
    key = settings.get('api').get('key', '')
    target = _build_target(settings, key)

    r = _request(target, key)
    print(r)


do_something()
