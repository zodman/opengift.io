from test_plus.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_Tracker, PM_Role
from PManager.viewsExt.public import Public
from PManager.viewsExt.tasks import taskListAjax
from PManager.views import MainPage
from tracker.urls import taskDetail
from django.utils.text import slugify
from django.utils.http import urlencode
import json

class ViewsTest(TestCase):
    def setUp(self):
        pm_tracker = mommy.make(PM_Tracker)
        for role in ('employee', 'manager', 'guest', 'client'):
            mommy.make(PM_Role, tracker=pm_tracker, code=role)
        self.make_user('user1')

    def test_pub(self):
        url = self.reverse(Public.mainPage)
        self.get_check_200(url)

    def test_create_project_tasks(self):
        with self.login(username='user1'):
            url = self.reverse(taskDetail)
            self.get_check_200(url)

            data = {
                'action': 'fastCreate',
                'project_id': '',
                'project_name': "Project 1",
                'project_description': 'Description 1',
                'project_code': slugify(u'Project 1'),
                'task_name': 'Project 1 - task 1',
                'task_description': 'Desc 1 '
            }
            resp = self.post(taskListAjax, data=data)
            self.response_200(resp)
            self.assertFalse("None" in resp.content, msg=resp.content)
            json_response = json.loads(resp.content)
            self.assertEqual(u"Project 1 - task 1", json_response.get("name"), msg=json_response)

            data = {'widgetList': ["task_edit"], 'activeMenuItem': 'tasks'}
            url = self.reverse(MainPage.indexRender, **data)
            querystring = {'id': json_response.get("id")}
            full_url = "{}?{}".format(url, urlencode(querystring))
            self.get_check_200(full_url)
            
