import requests

def url_request(url):
    response = requests.get(url)
    return response