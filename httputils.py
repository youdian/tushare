import urllib.request
from urllib.parse import urlencode
import sys

def get(url, params= None, headers= None):
    if params is not None:
        url += '?'
        url += urlencode(params)
    request = urllib.request.Request(url=url)
    if headers is not None:
        request = urllib.request.Request(url=url, headers = headers)
    response = urllib.request.urlopen(request)
    if response.code == 200:
        content = response.read().decode('utf-8')
        return content
    return None

if __name__ == '__main__':
    content = get(sys.argv[1])
    print(content)
