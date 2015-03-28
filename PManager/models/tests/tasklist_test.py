from django.test import TestCase
from PManager.models import TaskList
from PManager.models.tasks import PM_Project, PM_Tracker
from django.contrib.auth.models import User
from PManager.models.users import PM_User
import datetime

class TaskListTestCase(TestCase):
    def setUp(self):
    	self.tracker = PM_Tracker.objects.create(name="Heliant", code="heliant")
    	self.usr = User.objects.create(email="Test", password="123123")
        self.pro = PM_Project.objects.create(name="test", description="test", locked=0, author=self.usr, tracker=self.tracker)
        self.tlOpen = TaskList.objects.create(project=self.pro, status=1)
        self.tlClosed = TaskList.objects.create(project=self.pro, status=2)

    def test_tasklist_test(self):
        tlOpen = TaskList.objects.get(status=1)
        tlClosed = TaskList.objects.get(status=2)
        self.assertEqual(tlOpen.status, 1)
        self.assertEqual(tlClosed.status, 2)

    def test_tasklist_add_date_onclose(self):
    	tl = TaskList.objects.create(project=self.pro, status=1)
    	self.assertEqual(tl.status, 1)
    	tl.status = 2
    	tl.save()
    	tl2 = TaskList.objects.get(pk=tl.id)
    	self.assertIsNotNone(tl2.closed_at)


def log_(variable):
	print "######################"
	print str(variable)
	print "######################"