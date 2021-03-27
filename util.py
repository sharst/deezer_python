import time
import requests

def retried_get(url, retries=5, quota_wait=True):
    """ If quota_wait == True, wait for 5 seconds in case your quota was exceeded """
    for tries in range(retries):
        try:
            resp = requests.get(url).json()
            if quota_wait and 'error' in resp and resp['error']['code'] == 4:
                print('Quota exceeded, waiting for 5 seconds...')
                time.sleep(5)
                continue
            return resp
        except:
            print("Request to {} failed, retry {} of {}"\
                  .format(url, tries+1, retries))
