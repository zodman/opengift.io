__author__ = 'Gvammer'
import urllib, urllib2, json
from PManager.models import PM_Project
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
        coins = float(elem['amount (BTC)']) / float(coinRateInBtc)
        coins = round(coins, 4)
        try:
            project = PM_Project.objects.get(blockchain_name=projectCode)
            strCode += '<p>' + projectCode + ' ('+project.id+'): ' + elem['amount (BTC)'] + ' ('+str(coins)+' COIN)</p>'
        except PM_Project.DoesNotExist:
            pass


    return HttpResponse(strCode)