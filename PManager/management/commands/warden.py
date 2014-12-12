# -*- coding: utf-8 -*-
__author__ = 'Tonakai'
from tracker import settings
from django.core.management.base import BaseCommand
from optparse import Option
from PManager.classes.git.warden import Warden
import os
ROOT = os.path.normpath(os.path.dirname(__file__))
make_option = Option


class Command(BaseCommand):
    user = None
    repository = None
    warden = None
    option_list = BaseCommand.option_list + (
        make_option('--commits', action='store_true', dest='commits', help='Write commits to the message board'),
        make_option('--check', action='store_true', dest='check', help='Check for active task running'),
    )

    def handle(self, *args, **options):
        if not self.__get_user_and_repo(args):
            return 'ERROR: not enough arguments'
        try:
            self.warden = Warden(self.user, self.repository)
        except AssertionError:
            return 'ERROR: arguments failed to parse'
        if options['check']:
            return self.__check_active_tasks()
        if options['commits']:
            return self.__commits(args)

    def __get_user_and_repo(self, args):
        if len(args) < 2:
            return False
        if args[0]:
            self.user = args[0]
        if args[1]:
            self.repository = args[1]
        if self.user is None or self.repository is None:
            return False
        return True

    def __check_active_tasks(self):
        return self.warden.is_task()

    def __commits(self, args):
        if len(args) > 2 and args[2]:
            ref = args[2]
        else:
            return 'ERROR:ref not specified'
        hashes = []
        if len(args) > 3 and args[3]:
            for i in range(3, len(args)):
                hashes.append(args[i])
        if not hashes:
            print u'ERROR:Commits not found for ref:{0:s}'.format(ref)
            return 'false'
        print u'Committing message for ref:{0:s}'.format(ref)
        print u'Commits hashes: {0:s}'.format(hashes)
        return self.warden.write_message(hashes=hashes, ref=ref)



