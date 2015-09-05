import urllib
import json

API_KEY = 'Hy2RqHeWjiYwSGns53L51DqL'
SECRET_KEY = 'ogwLIpoz5QyVP7ox1R0E5tx6qqdGTF3a'
ACCESS_TOKEN = '24.f87191642b190394b6aae95f5be9d302.2592000.1442556270.282335-6657846'


def get_tokens():
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    params = urllib.urlencode(params)
    r = urllib.urlopen('https://openapi.baidu.com/oauth/2.0/token?' + params)
    d = json.load(r.read())
    return d['access_token'], d['refresh_token']


def upload(filename, des):
    params = {
        'method': 'upload',
        'access_token': ACCESS_TOKEN,
        'path': des,
        'ondup': 'overwrite'
    }
    qs = urllib.urlencode(params)

    with open(filename, 'rb') as f:
        data = urllib.urlencode({'file': f.read()})
        r = urllib.urlopen('https://c.pcs.baidu.com/rest/2.0/pcs/file?' + qs, data)
        print r.code
        print json.loads(r.read())
