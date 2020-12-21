import yaml


def configuration():
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.load(stream, Loader=yaml.SafeLoader).get('buckets_settings', {})
            token = settings.get('api').get('key', '')
            access_key = settings.get('bucket_keys').get('access_key', '')
            secret_key = settings.get('bucket_keys').get('secret_key', '')
            return settings, token, access_key, secret_key
        except yaml.YAMLError as exception:
            print(exception)
