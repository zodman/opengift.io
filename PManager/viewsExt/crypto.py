__author__ = 'Gvammer'
import urllib, urllib2, json
CRYPTO_HOST = '188.166.237.19'

def bitcoin_set_request(project_id, sum):
    service_url = '/bitcoin/request/create'

    fp = urllib.request.urlopen("http://" + CRYPTO_HOST + service_url + '?project='+str(project_id)+'&sum='+str(sum))
    mybytes = fp.read()

    res = mybytes.decode("utf8")
    fp.close()

    return json.loads(res)