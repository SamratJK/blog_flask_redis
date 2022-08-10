import requests
def count_words_at_url(url):
    resp = requests.get(url)
    for i in range(0,10):
        print('lol')
    return len(resp.text.split())