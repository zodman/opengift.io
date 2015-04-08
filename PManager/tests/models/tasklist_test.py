from django.test import TestCase
from PManager.models import TaskList
from PManager.models.tasks import PM_Project, PM_Tracker, PM_Task
from django.contrib.auth.models import User
from PManager.models.users import PM_User
import datetime

class TaskListTestCase(TestCase):
    def setUp(self):
    	self.tracker = PM_Tracker.objects.create(name="Heliant", code="heliant")
        self.usr = User.objects.create(username="test1", email="test@test.com", password="123123")
        self.usr2 = User.objects.create(username="test2", email="test2@test.com", password="123123")
        self.pro = PM_Project.objects.create(name="test", description="test", locked=0, author=self.usr, tracker=self.tracker)
        self.task1 = PM_Task.objects.create(name="TEST TASK 1", project=self.pro, author=self.usr)
        self.task2 = PM_Task.objects.create(name="TEST TASK 2", project=self.pro, author=self.usr)

    def test_tasklist_test(self):
        tl = TaskList.objects.create(project=self.pro)
        self.assertIsNotNone(tl.pk, "TaskList should be saved properly")
        self.assertEqual(tl.status, TaskList.CLOSED, "TaskList should be created with default closed status")

    def test_tasklist_closed_at_should_be_null_at_start(self):
        tl = TaskList.objects.create(project=self.pro)
        self.assertIsNone(tl.closed_at, "Closed_at field should not be setted immedietly after creation")

    def test_tasklist_forced_close_if_empty_tasks_or_users(self):
        tl = TaskList.objects.create(project=self.pro, status=TaskList.OPEN)
        self.assertEqual(tl.status, TaskList.CLOSED, "Status should be closed after list creation")
        tl.status = TaskList.OPEN
        tl.save()
        tl2 = TaskList.objects.get(pk=tl.id)
        self.assertEqual(tl2.status, TaskList.CLOSED, "TaskList should be saved with forced data on pre_save signal")

    def test_should_not_add_closed_at_at_second_save(self):
        tl = TaskList.objects.create(project=self.pro)
        tl.save()
        self.assertIsNone(tl.closed_at, "Closed_at field should not be setted on re-save")        
        tl.status = TaskList.CLOSED
        tl.save()
        self.assertIsNone(tl.closed_at, "Closed_at field should not be setted on re-save")        

    def test_tasklist_would_open(self):
        tl = TaskList.objects.create(project=self.pro)
        tl.users.add(self.usr)
        tl.tasks.add(self.task1)
        tl.status = TaskList.OPEN
        tl.save()
        self.assertEqual(tl.status, TaskList.OPEN)

    def test_tasklist_closing_should_set_closed_at(self):
        tl = TaskList.objects.create(project=self.pro)
        self.assertIsNone(tl.closed_at)
        tl.users.add(self.usr)
        tl.tasks.add(self.task1)
        tl.status = TaskList.OPEN
        tl.save()
        self.assertIsNone(tl.closed_at)
        tl.status = TaskList.CLOSED
        tl.save()
        self.assertIsNotNone(tl.closed_at)

    def test_tasklist_add_users_and_tasks(self):
        #default status should be closed
    	tl = TaskList.objects.create(project=self.pro)
    	self.assertEqual(tl.status, TaskList.CLOSED)
    	tl.tasks.add(self.task1)
        tl.users.add(self.usr)
        tl.status = TaskList.OPEN
    	tl.save()
        #status with tasks and users should be open
        self.assertEqual(tl.status, TaskList.OPEN)
    	tl2 = TaskList.objects.get(pk=tl.id)
        self.assertIsNotNone(tl2.users)
        self.assertIsNotNone(tl2.tasks)

    def test_tasklist_close_on_empty_tasks(self):
        tl = TaskList.objects.create(project=self.pro)
