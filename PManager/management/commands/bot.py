# -*- coding: utf-8 -*-
__author__ = 'Gvammer'
from django.core.management.base import BaseCommand

import telebot

class Command(BaseCommand):
    def handle_noargs(self, **options):
        bot = telebot.TeleBot('553153292:AAGtveJ6JhmNWuuKUiNWwEcL5a8-12z0TRs')

        @bot.message_handler(func=lambda message: True, content_types=['text'])
        def echo_message(message):
            bot.reply_to(message, message.text)

        print "----------START------------"
        bot.polling(none_stop=True)


