import requests

def retried_get(url, retries=5):
    for tries in range(retries):
        try:
            return requests.get(url).json()
        except:
            print("Request to {} failed, retry {} of {}"\
                  .format(url, tries+1, retries))
