__author__ = 'Gvammer'
import urllib, urllib2, json
from PManager.models import PM_Project
from PManager.services.danations import donate
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User

CRYPTO_HOST = '188.166.237.19'

def get_rate():
    fp = urllib.urlopen("https://blockchain.info/tobtc?currency=USD&value=0.2")
    res = fp.read()
    coinRateInBtc = float(res)
    return coinRateInBtc

def bitcoin_set_request(project_name, sum):
    service_url = '/bitcoin/request/create'

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url + '?project='+str(project_name)+'&sum='+str(sum))
    res = fp.read()

    return json.loads(res)

def get_paid_btc():
    service_url = '/bitcoin/request/paid'
    service_url_clear = '/bitcoin/request/clear'

    coinRateInBtc = get_rate()

    exchangeName = 'opengift@opengift.io'

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url)
    res = fp.read()
    res = json.loads(res)
    strCode = 'start '+"\r\n"

    for elem in res:
        donateCode = elem['memo'].split(':')
        projectCode = donateCode.pop()
        userId = donateCode.pop()
        user = None
        try:
            user = User.objects.get(pk=int(userId))
        except ValueError, User.DoesNotExist:
            pass

        coins = float(elem['amount (BTC)']) / float(coinRateInBtc)
        coins = round(coins, 4)
        try:
            project = PM_Project.objects.get(blockchain_name=projectCode)
            strCode += '' + projectCode + ' ['+str(project.id)+']: ' + elem['amount (BTC)'] + ' BTC ('+str(coins)+' COIN)'+"\r\n"
            if donate(coins, project, user, None, exchangeName):
                urllib.urlopen("http://" + CRYPTO_HOST + service_url_clear + '?address='+elem['address'])
            else:
                strCode += "failed to donate to "+project.blockchain_name+"\r\n"

        except PM_Project.DoesNotExist:
            pass

    fd = open('log/crypto/btcRead.log', "a")
    fd.write(strCode)
    fd.close()

    return strCode