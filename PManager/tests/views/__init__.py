from test_plus.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_Tracker, PM_Role, PM_Task
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

    def test_create_project_task(self):
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

            # check deadline
            pm_task = PM_Task.objects.all()[0]
            self.assertNotEqual(pm_task.deadline, None)
            # when first result send the deadline will removed
            data = {
                'message_type':"result",
                'to':'',
                'winner':'',
                'need-time-hours':'', 
                'task_id': pm_task.id,
                'task_message': 'Message result',
                'file':'' 
            }
            resp = self.post(taskListAjax,data=data)
            self.response_200(resp)
            pmtask = PM_Task.objects.get(id=pm_task.id)
            self.assertEqual(pmtask.deadline,None)

    def test_task_handler_action_all(self):
        #Make public the tag FooBAR
        mommy.make('PManager.Tags', tagText='FOOBAR', is_public=True)
        with self.login(username='user1'):
            data = {
                'action': 'fastCreate',
                'project_id': '',
                'project_name': "Project 1",
                'project_description': 'Description 1',
                'project_code': slugify(u'Project 1'),
                'task_name': 'task number one',
                'task_description': 'Desc foobar'
            }
            resp = self.post(taskListAjax, data=data)
            self.response_200(resp)
            json_response = json.loads(resp.content)
            self.assertTrue(json_response.get("project"), msg=json_response.get("project"))


            # check if load
            self.get_check_200(MainPage.projectWidgets)
            post_data = {
                'page':1,
                'action':'all',
                'project':0,
            }
            resp = self.post('task-handler', data=post_data)
            self.response_200()
            data = json.loads(resp.content)
            
            # check for task
            tasks = data.get("tasks",[])
            self.assertEqual(len(tasks), 1)
            task = data.get("tasks")[0]
            # check if task contain tags
            tags = [i['tagText'] for i in task.get("tags")]
            self.assertTrue('FOOBAR' in tags , msg=task.get("tags"))

           # check if search

            post_data = {
                'page':1,
                'action':'all',
                'project':0,
                'tag_search':['FOOBAR',],
            }
            resp = self.post('task-handler', data=post_data)
            self.response_200()
            data = json.loads(resp.content)
            self.assertEqual(len(data.get("tasks")), 1, msg='notasks')

