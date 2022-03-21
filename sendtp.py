import urllib.request
import base64
import os
import json

base_url = 'https://api.typingdna.com'
apiKey = os.getenv('tpkey')
apiSecret = os.getenv('tpsecret')


def send_typing_data(user_id, pattern):
    print(user_id)
    print(pattern)
    authstring = f"{apiKey}:{apiSecret}"
    base64string = base64.decodebytes(
        authstring.encode()).decode().replace('\n', '')
    data = urllib.parse.urlencode({'tp': pattern})
    url = f'{base_url}/auto/{user_id}'

    request = urllib.request.Request(url, data.encode('utf-8'), method='POST')
    request.add_header("Authorization", f"Basic {base64string}")
    request.add_header("Content-type", "application/x-www-form-urlencoded")

    res = urllib.request.urlopen(request)
    res_body = res.read()
    return json.loads(res_body.decode('utf-8'))