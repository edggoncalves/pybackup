import urllib3
import json


def request(target, token):
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
