__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect
from PManager.models import PM_User, PM_Project, PM_Milestone
from PManager.viewsExt.crypto import bitcoin_set_request, get_rate
from PManager.services.danations import donate
from django.template import loader, RequestContext
from PManager.services.docker import blockchain_project_status_request, blockchain_goal_confirmation_request, \
    blockchain_token_move_request, blockchain_pay_request, blockchain_project_getbalance_request, \
    blockchain_user_newproject_request, blockchain_user_register_request, blockchain_user_getkey_request, \
    blockchain_user_getbalance_request
from tracker.settings import GIFT_USD_RATE


def blockchainMain(request):
    import urllib
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?backurl=' + urllib.quote(request.get_full_path()))

    sum = request.user.get_profile().get_donation_sum()
    next_level_sum = 1000
    next_level = None

    for k, v in PM_User.level_sum.iteritems():
        if sum > v:
            sum -= v
        else:
            next_level_sum = v
            next_level = k
            break

    c = RequestContext(request, {
        'donator_level': request.user.get_profile().opengifter_level,
        'donator_level_percent': sum * 100 / next_level_sum,
        'donator_next_level': next_level
    })

    return HttpResponse(loader.get_template('blockchain/index.html').render(c))


def userRegisterAndUpdate(request):
    result = blockchain_user_register_request(request.user.username)
    if result.find('Error') == -1:
        res = result.split("\n\n")
        profile = request.user.get_profile()

        profile.blockchain_key = res[0]
        profile.blockchain_cert = res[1]
        profile.blockchain_wallet = blockchain_user_getkey_request(request.user.username)
        profile.save()

        return 'ok'
    return False


def blockchainIncome(request):
    import json
    fd = open('logCrypto.log', "a")
    fd.write(json.dumps(request.POST))
    fd.write("\r\n")
    fd.close()
    return HttpResponse('ok')


def blockchainAjax(request):
    action = request.POST.get('action')
    result = ''
    if action == 'register':
        result = userRegisterAndUpdate(request)

    elif action == 'getKey':
        profile = request.user.get_profile()

        if profile.blockchain_wallet:
            result = profile.blockchain_wallet
        else:
            profile.blockchain_wallet = blockchain_user_getkey_request(request.user.username)
            profile.save()

    elif action == 'getBalance':
        profile = request.user.get_profile()
        wallet = profile.blockchain_wallet
        result = blockchain_user_getbalance_request(request.user.username, wallet)

    elif action == 'confirmGoal':
        project = int(request.POST.get('projectId'))
        try:
            project = PM_Project.objects.get(pk=project)
            goal = int(request.POST.get('goalId'))
            result = blockchain_goal_confirmation_request(
                request.user.username,
                project.blockchain_name,
                'opengift.io:' + str(goal)
            )

        except PM_Project.DoesNotExist:
            result = 'Error: Project  does not exists'

    elif action == 'addProject':
        # profile = request.user.get_profile()
        project = int(request.POST.get('id'))
        name = request.POST.get('name')
        if name and project:
            try:
                project = PM_Project.objects.get(pk=project)
                if request.user.get_profile().blockchain_wallet:
                    result = blockchain_user_newproject_request(request.user.username, name)
                    if result == 'ok':
                        project.blockchain_name = name
                        project.save()
            except PM_Project.DoesNotExist:
                result = 'error'

    elif action == 'pay':
        # profile = request.user.get_profile()
        wallet = request.POST.get('wallet')
        sum = request.POST.get('sum')
        result = blockchain_pay_request(request.user.username, wallet, sum)

    elif action == 'move':
        # profile = request.user.get_profile()
        project = request.POST.get('project')
        qty = request.POST.get('qty')
        wallet = request.POST.get('wallet')
        result = blockchain_token_move_request(request.user.username, project, wallet, qty)

    elif action == 'donate':
        import json
        # profile = request.user.get_profile()
        project = request.POST.get('project')
        milestone = request.POST.get('milestone', None)
        try:
            project = PM_Project.objects.get(blockchain_name=project)
        except PM_Project.DoesNotExist:
            return HttpResponse('Fatal error: projects does not exist')

        if milestone:
            try:
                milestone = PM_Milestone.objects.get(pk=int(milestone))
            except PM_Milestone.DoesNotExist:
                pass

        ref = request.COOKIES.get('ref')
        refUser = None
        if ref:
            try:
                refUser = PM_User.objects.get(blockchain_wallet=ref)
            except PM_User.DoesNotExist:
                pass

        qty = float(request.POST.get('qty', 0))
        currency = request.POST.get('currency', 'gift')
        uid = request.user.id if request.user.is_authenticated() else '-1'
        if currency == 'gift':
            if refUser and refUser.id != uid:
                qtyRef = qty * 0.2
                blockchain_pay_request(
                    request.user.username,
                    refUser.blockchain_wallet,
                    qtyRef
                )
                qty -= qtyRef

            result = donate(
                qty,
                project,
                request.user,
                milestone,
                None,
                refUser.user if refUser else None
            )

        elif currency == 'btc':
            result = bitcoin_set_request(
                ':'.join(
                    [
                        project.blockchain_name,
                        str(uid),
                        (str(milestone.id) if milestone else '-1'),
                        (str(refUser.id) if refUser else '0')
                    ]
                ),
                qty
            )
            result = json.dumps(result)

        elif currency == 'usd':
            import paypalrestsdk
            my_api = paypalrestsdk.Api({
                'mode': 'sandbox',
                'client_id': 'ARKZ_toXISzJ4LOFQ095nMuPqlRloVI1WNwDMfTEUL-YQzDOif9V6AhgMlQ-SKGT1l7VAGUu0clfT4oR',
                'client_secret': 'EHJ-uDfarrQjQukYceH7HEX-bNWe0GBrvKWpvnX9EF4JJeSyoC_K3UQdukDRBbilJXT3FHnX7asSQ2Z5'
            })
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": "http://opengift.dev/paypal/",
                    "cancel_url": "http://opengift.dev/"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": project.name + " donation",
                            "sku": (str(milestone.id) if milestone else '-1'),
                            "price": str(qty),
                            "currency": "USD",
                            "quantity": 1
                        }]},
                    "amount": {
                        "total": str(qty),
                        "currency": "USD"},
                    "description": "This is the payment transaction description."}
                ]}, api=my_api)
            approval_url = ''
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        # Convert to str to avoid Google App Engine Unicode issue
                        # https://github.com/paypal/rest-api-sdk-python/pull/58
                        approval_url = str(link.href)
            # result = bitcoin_set_request(
            #     ':'.join(
            #         [
            #             project.blockchain_name,
            #             str(uid),
            #             (str(milestone.id) if milestone else '-1'),
            #             (str(refUser.id) if refUser else '0')
            #         ]
            #     ),
            #     qty
            # )
            result = json.dumps(approval_url)

    elif action == 'getRate':
        currency = request.POST.get('currency', None)
        if currency == 'btc':
            result = get_rate()
        elif currency == 'gift':
            result = 1.0 / GIFT_USD_RATE
        else:
            result = 'Incorrect currency'

    elif action == 'getProjectVals':
        # profile = request.user.get_profile()
        project = request.POST.get('pName')
        result = blockchain_project_getbalance_request('gvammer', project)

    elif action == 'getProjectStatus':
        # profile = request.user.get_profile()
        project = request.POST.get('pName')
        result = blockchain_project_status_request(request.user.username, project)

    return HttpResponse(result)

def paypalExecute(request):
    from paypalrestsdk import Payment
    paymentId = request.GET.get('payentId')
    payerId = request.GET.get('PayerID')
    if paymentId and payerId:
        # Payment id obtained when creating the payment (following redirect)
        payment = Payment.find(paymentId)

        # Execute payment using payer_id obtained when creating the payment (following redirect)
        if payment.execute({"payer_id": payerId}):
          return HttpResponse("Payment[%s] execute successfully" % (payment.id))
        else:
          return HttpResponse(payment.error)
