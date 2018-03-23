__author__ = 'Gvammer'
import urllib, urllib2, json
from PManager.models import PM_Project, PM_Milestone, PM_User, PM_Task
from PManager.services.danations import donate
from PManager.services.docker import blockchain_pay_request
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from tracker.settings import GIFT_USD_RATE

CRYPTO_HOST = '188.166.237.19'


def get_rate():
    fp = urllib.urlopen("https://blockchain.info/tobtc?currency=USD&value=1")
    res = fp.read()
    coinRateInBtc = float(res)
    return "{0:.8f}".format(coinRateInBtc)


def bitcoin_set_request(project_name, sum, milestone=None):
    service_url = '/bitcoin/request/create'

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url + '?project=' + str(project_name) + '&sum=' + str(sum))
    res = fp.read()

    return json.loads(res)


def get_paid_btc():
    service_url = '/bitcoin/request/paid'
    all_url = '/bitcoin/request/list.json'
    service_url_clear = '/bitcoin/request/clear'

    coinRateInBtc = float(get_rate()) * GIFT_USD_RATE

    exchangeName = 'opengift@opengift.io'

    fp = urllib.urlopen("http://" + CRYPTO_HOST + service_url)
    res = fp.read()
    res = json.loads(res)
    strCode = 'start ' + "\r\n"
    if res:
        for elem in res:
            donateCode = elem['memo'].split(':')
            refUserId = donateCode.pop()
            milestoneId = donateCode.pop()
            userId = donateCode.pop()
            projectCode = donateCode.pop()

            user = None
            try:
                user = User.objects.get(pk=int(userId))
            except ValueError, User.DoesNotExist:
                pass

            milestone = None
            task = None
            try:
                milestone = PM_Milestone.objects.get(pk=milestoneId)
            except ValueError, PM_Milestone.DoesNotExist:
                try:
                    task = PM_Task.objects.get(pk=int(milestoneId.replace('t', '')))
                except ValueError, PM_Task.DoesNotExist:
                    pass

            coins = float(elem['amount (BTC)']) / float(coinRateInBtc)
            coins = round(coins, 4)
            try:
                project = PM_Project.objects.get(blockchain_name=projectCode)
                strCode += '' + projectCode + ' [' + str(project.id) + ']: ' + elem['amount (BTC)'] + ' BTC (' + str(
                    coins) + ' COIN)' + "\r\n"

                refUser = None
                if refUserId:
                    try:
                        refUser = PM_User.objects.get(pk=refUserId)
                        qtyRef = coins * 0.2
                        blockchain_pay_request(exchangeName, refUser.blockchain_wallet, qtyRef)
                        coins -= qtyRef

                    except PM_User.DoesNotExist:
                        pass

                if donate(coins, project, user, milestone, exchangeName, refUser.user, task):
                    urllib.urlopen("http://" + CRYPTO_HOST + service_url_clear + '?address=' + elem['address'])
                else:
                    strCode += "failed to donate to " + project.blockchain_name + "\r\n"

            except PM_Project.DoesNotExist:
                pass

    fp = urllib.urlopen("http://" + CRYPTO_HOST + all_url)
    res = fp.read()
    res = json.loads(res)
    for elem in res:
        if elem['status'] == 'Expired':
            urllib.urlopen("http://" + CRYPTO_HOST + service_url_clear + '?address=' + elem['address'])
            strCode += "Cleared expired " + elem['address'] + "\r\n"

    fd = open('log/crypto/btcRead.log', "a")
    fd.write(strCode)
    fd.close()

    return strCode
