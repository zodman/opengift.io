__author__ = 'Gvammer'
import urllib, urllib2, json
from django.shortcuts import HttpResponse
CRYPTO_HOST = '188.166.237.19'

def bitcoin_set_request(project_id, sum):
    service_url = '/bitcoin/request/create'

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url + '?project='+str(project_id)+'&sum='+str(sum))
    res = fp.read()

    return json.loads(res)

def get_paid_btc(request):
    service_url = '/bitcoin/request/paid'

    fp = urllib.urlopen("https://blockchain.info/tobtc?currency=USD&value=0.2")
    res = fp.read()
    coinRateInBtc = json.loads(res)

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url)
    res = fp.read()
    res = json.loads(res)
    strCode = ''
    for elem in res:
        projectCode = elem['memo'].split(':').pop()
        strCode += '<p>' + projectCode + ': ' + elem['amount (BTC)'] + ' ('+str(float(elem['amount (BTC)']) / float(coinRateInBtc))+' COIN)</p>'


    return HttpResponse(strCode)