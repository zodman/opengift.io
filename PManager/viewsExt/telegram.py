__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
import telebot

WEBHOOK_HOST = 'opengift.io'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

token = '553153292:AAGtveJ6JhmNWuuKUiNWwEcL5a8-12z0TRs'


def botPage(request):
    bot = telebot.TeleBot(token)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def echo_message(message):
        bot.reply_to(message, message.text)

    if True:
        import json
        body_unicode = request.body.decode('utf-8')
        f = open('/home/opengift/web/logbot.log', 'a+')
        f.write(body_unicode)
        f.close()
        body = json.loads(body_unicode)
        update = telebot.types.Update.de_json(body)

        bot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise Exception
