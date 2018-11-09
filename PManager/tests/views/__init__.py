from test_plus.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User
from PManager.models import PM_Project
from PManager.viewsExt.public import Public

class ViewsTest(TestCase):
    def setUp(self):
        self.usr = mommy.make(User)
        self.project = mommy.make(PM_Project)

    def test_pub(self):
        url = self.reverse(Public.mainPage)
        self.get_check_200(url)
