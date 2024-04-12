import base64
import requests
import os

os.environ['REQUESTS_CA_BUNDLE'] = 'C:/Users/AU256UR/Downloads/Zscaler Root CA.crt'

with open("../static/images/sample/aws_arch_sample_01.png", "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": 'e601a932b245c10cc0ecf3db7b177bdf',
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)

    print(res.json())