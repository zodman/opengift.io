# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.viewsExt.crypto import get_paid_btc
from PManager.models import PM_Project


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for p in PM_Project.objects.filter(blockchain_name__isnull=True):
            rating = 0
            rating += p.milestones.count()
            industries = p.industries.count()

            if industries > 5:
                industries = 5

            rating += industries
            rating += p.problems.count()
            if p.link_site:
                rating += 1

            if p.link_github:
                rating += 1

            if p.link_demo:
                rating += 1

            if p.link_video:
                rating += 1

            rating += p.getUsers().count()

            p.opengift_rating = rating
            p.save()