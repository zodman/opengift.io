__author__ = 'Gvammer'
import urllib, urllib2, json
CRYPTO_HOST = '188.166.237.19'

def bitcoin_set_request(project_id, sum):
    service_url = '/bitcoin/request/create'

    url = "http://" + CRYPTO_HOST + service_url
    req = urllib2.Request(url, '?project='+str(project_id)+'&sum='+str(sum))
    result = urllib2.urlopen(req)
    res = result.read()

    return json.loads(res)