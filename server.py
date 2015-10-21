# -*- coding:utf-8 -*-
#!/usr/bin/env python
__author__ = 'Gvammer'

from tornado import gen
from tornadio2 import SocketConnection, event
import os, json, datetime, re, django.contrib.auth, django.utils, django.conf
import tornadoredis
import tracker.settings as settings
from django.utils import timezone
from PManager.viewsExt.tools import templateTools
from PManager.widgets.tasklist.widget import widget as taskList
from PManager.models import PM_Task_Message, PM_Files, PM_Task, PM_Timer
from django.db import transaction
from PManager.classes.server.message import ServerMessage

ROOT = os.path.normpath(os.path.dirname(__file__))

ORDERS_FREE_LOCK_TIME = getattr(settings, 'ORDERS_FREE_LOCK_TIME', 0)
ORDERS_REDIS_HOST = getattr(settings, 'ORDERS_REDIS_HOST', 'localhost')
ORDERS_REDIS_PORT = getattr(settings, 'ORDERS_REDIS_PORT', 6379)
ORDERS_REDIS_PASSWORD = getattr(settings, 'ORDERS_REDIS_PASSWORD', None)
ORDERS_REDIS_DB = getattr(settings, 'ORDERS_REDIS_DB', 0)


@transaction.commit_manually
def flush_transaction():
    transaction.commit()


onlineUsers = {}


class PM_Tasks_Connector():
    def __init__(self):
        flush_transaction()

    def getTask(self, id, user):
        try:
            taskListArray = taskList(user, {},
                                     {
                                         'filter': {
                                             'pk': id
                                         }
                                     })
            if 'tasks' in taskListArray:
                tasks = taskListArray['tasks']

                if tasks:
                    task = list(tasks)[0]

                    return json.dumps(task)
                else:
                    return 'Not exist'
        except PM_Task.DoesNotExist:
            pass

    def getMessage(self, id, cur_user):
        try:
            message = PM_Task_Message.objects.get(pk=id)
            if message.canView(cur_user):
                return json.dumps(message.getJson(None, cur_user))

        except PM_Task_Message.DoesNotExist:
            return json.dumps({'message': 'Message does not exist'})

    def deleteMessage(self, id, user):
        try:
            mess = PM_Task_Message.objects.get(pk=id)

            if mess.canDelete(user):
                mess.delete()
                return 'Message has been deleted'
            else:
                return 'Failed to delete'

        except PM_Task_Message.DoesNotExist:
            return 'Message not found'

    def addMessage(self, messageData, user):
        if user:
            message = PM_Task_Message()
            message.updateFromRequestData(messageData, user)
            message.author = user
            message.save()

            return json.dumps({
                'id': message.id
            })

    def updateMessage(self, messageData, user):
        try:
            if 'id' in messageData:
                message = PM_Task_Message.objects.get(pk=messageData['id'])

                if message.updateFromRequestData(messageData, user):
                    message.modifiedBy = user
                    message.save()

                return json.dumps({
                    'id': message.id
                })

        except PM_Task_Message.DoesNotExist:
            return 'Message Not found'

    def profileHaveAccess(self, profile, task, message="view"):
        if not isinstance(task, PM_Task):
            try:
                task = PM_Task.objects.get(pk=int(task))
            except PM_Task.DoesNotExist:
                pass
            ##########
        return profile.hasAccess(task, message)

    def userHaveAccess(self, user, task, message="view"):
        if not isinstance(task, PM_Task):
            try:
                task = PM_Task.objects.get(pk=int(task))
            except PM_Task.DoesNotExist:
                pass
            ##########
        return user.get_profile().hasAccess(task, message)

    def stopTimer(self, userId):
        try:
            timer = PM_Timer.objects \
                .get(user=userId, dateEnd__isnull=True)
            timer.task.Stop()
            timer.task.endTimer(user=userId, comment='Disconnect')

        except PM_Timer.DoesNotExist:
            return False

# Declare connection class
class MyConnection(SocketConnection):
    id = None
    user = None
    profile = None
    uniqueId = None

    def __init__(self, *args, **kwargs):
        super(MyConnection, self).__init__(*args, **kwargs)
        self.listen_redis()

    def close(self):
        try:
            self.redis_client.disconnect()
        except Exception:
            pass
        super(MyConnection, self).close()

    @gen.engine
    def listen_redis(self):
        """
        Вешаем подписчиков на каналы сообщений.
        """
        self.redis_client = tornadoredis.Client(
            host=ORDERS_REDIS_HOST,
            port=ORDERS_REDIS_PORT,
            password=ORDERS_REDIS_PASSWORD,
            selected_db=ORDERS_REDIS_DB
        )
        self.redis_client.connect()

        yield gen.Task(self.redis_client.subscribe, [
            're.task.update',
            're.comment.add'
        ])
        self.redis_client.listen(self.on_redis_queue)  # при получении сообщения
        #  вызываем self.on_redis_queue

    #быстрая отправка системного сообщения текущему соединению
    def systemMessage(self, message):
        self.emit('message', json.dumps({
            'message': message,
            'user': 'Система',
            'date': templateTools.dateTime.convertToSite(datetime.datetime.now())
        }))

    #получениие сообщения от redis
    def on_redis_queue(self, message):
        if message.kind == 'message':
            # сообщения у редиса бывают разного типа,
            # много сервисных, нам нужны только эти
            # к модели Task_Message это условие отношения не имеет
            message_body = json.loads(message.body)

            if hasattr(self, 'id'):

                taskConnector = PM_Tasks_Connector()
                userId = message_body['user'] if 'user' in message_body else None

                serverMessage = ServerMessage.getFromRedisMessage(message, self)

                if serverMessage and serverMessage.id and (userId != self.id or not userId):
                    if serverMessage.objectName == 'task':
                        if self.user and taskConnector.profileHaveAccess(self.profile, serverMessage.id):
                            serverMessage.send()
                    elif serverMessage.objectName == 'comment':
                        try:
                            serverMessage.send()
                        except PM_Task_Message.DoesNotExist:
                            pass

                del serverMessage

    def on_open(self, info):
        pass

    def on_message(self, msg):
        self.send(msg)

    def on_close(self):
        global onlineUsers

        if self.id in onlineUsers:
            if self.uniqueId in onlineUsers[self.id]:
                #onlineUsers[self.id][self.uniqueId].close()
                del onlineUsers[self.id][self.uniqueId]

                if len(onlineUsers[self.id]) == 0:
                    del onlineUsers[self.id]

        if not self.id in onlineUsers:
            conn = PM_Tasks_Connector()
            conn.stopTimer(self.id)

    @event('task:read')
    def putTask(self, *args, **kags):
        if 'id' in kags:
            id = int(kags['id'])
            conn = PM_Tasks_Connector()
            return conn.getTask(id, self.user)

    @event('message:read')
    def putMessage(self, *args, **kags):
        if 'id' in kags:
            id = int(kags['id'])
            conn = PM_Tasks_Connector()
            return conn.getMessage(id, self.user)
        else:
            return "Can't find ID in request"

    @event('message:delete')
    def deleteMessage(self, *args, **kags):
        if 'id' in kags:
            id = int(kags['id'])
            conn = PM_Tasks_Connector()
            return conn.deleteMessage(id, self.user)
        else:
            return 'Model must have ID'

    @event('message:create')
    def saveMessage(self, *args, **kags):
        if 'text' in kags:
            conn = PM_Tasks_Connector()
            return conn.addMessage(kags, self.user)

    @event('message:update')
    def updateMessage(self, *args, **kags):
        if 'id' in kags:
            conn = PM_Tasks_Connector()
            return conn.updateMessage(kags, self.user)

    @event('chat_message')
    def receiveMessage(self, data):
        message = PM_Task_Message(text=data, author=self.user)
        message.save()
        file = False

        if '#' in data:
            strExpr = '\#([0-9]+)\#'
            link_re = re.compile(strExpr)
            file_id = link_re.findall(data)
            if file_id and file_id[0]:
                file_id = int(file_id[0])
                file = PM_Files.objects.get(pk=file_id)

                if file_id and file:
                    message.files.add(file_id)

            data = re.sub(strExpr, '', data)

        toJson = {
            'message': data,
            'date': datetime.datetime.now().strftime('%I:%M:%S, %d.%m.%Y'),
            'user': self.user.username
        }
        if file:
            toJson['img'] = str(file.file).replace('PManager', '')

        self.broadcast('message', json.dumps(toJson))

    @event('users:get_online_list')
    def getOnlineUsers(self, data):
        return json.dumps(self.getOnlineUsersList())

    def getOnlineUsersList(self):
        global onlineUsers
        arUsers = []
        if onlineUsers:
            for i in onlineUsers:
                for k in onlineUsers[i]:
                    firstUserHandle = onlineUsers[i][k]

                    if firstUserHandle.user:
                        arUsers.append(self.userData(firstUserHandle.user, 'online'))

            return arUsers

    @event('users:get_user_data')
    def getUserData(self, id):
        global onlineUsers

        if id in onlineUsers:
            for k in onlineUsers[id]:
                return self.userJsonData(onlineUsers[id][k].user, 'online')

    @event('connect')
    def connect(self, sessionid):
        import random, time

        global onlineUsers, tornadoDjangoSessions

        if sessionid:
            self.djangosession = self.get_django_session(sessionid)
            if self.djangosession:
                class Dummy(object):
                    pass

                django_request = Dummy()
                django_request.session = self.djangosession
                user = django.contrib.auth.get_user(django_request)

                if user.is_authenticated():

                    self.id = user.id
                    self.user = user
                    self.profile = user.get_profile()
                    self.uniqueId = str(random.random()) + str(time.time())

                    if self.id in onlineUsers:
                        onlineUsers[self.user.id][self.uniqueId] = self
                    else:
                        onlineUsers[self.user.id] = {self.uniqueId: self}

                    self.broadcast('userLogin', self.userJsonData(self.user,
                                                                  'online')) #рассылаем всем онлайн-юзерам инфу о новом юзере

            return 'Connected'

        return 'Session not found'

    def userJsonData(self, user, status):
        return json.dumps(self.userData(user, status))

    def userData(self, user, status):
        return {
            'id': user.id,
            'username': user.username,
            'status': status
        }

    def get_django_session(self, session_key):
        if not hasattr(self, 'djangosession'):
            engine = django.utils.importlib.import_module(django.conf.settings.SESSION_ENGINE)
            self.djangosession = engine.SessionStore(session_key)
        return self.djangosession

    def broadcast(self, event, data):
        global onlineUsers
        if onlineUsers:
            for i in onlineUsers:
                for k in onlineUsers[i]:
                    onlineUsers[i][k].emit(event, data)