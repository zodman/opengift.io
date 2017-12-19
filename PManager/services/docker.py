# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
import urllib
import urllib2
import json
from tracker.settings import DOCKER_HOST, DOCKER_APP_KEY
from PManager.models.interfaces import AccessInterface

def blockchain_donate_request(username, project, qty):
    result = __blockchain_request_raw('/blockchain/write', {'user': username, 'fcn': 'donate', 'arg1': project.lower(), 'arg2': qty})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to token move ' + username + '('+result+')'

    # result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return 'ok'

def blockchain_token_move_request(username, project, wallet, qty):
    result = __blockchain_request_raw('/blockchain/write', {'user': username, 'fcn': 'move', 'arg1': project, 'arg2': wallet, 'arg3': qty})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to token move ' + username

    # result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return 'ok'

def blockchain_pay_request(username, wallet, sum):
    result = __blockchain_request_raw('/blockchain/write', {'user': username, 'fcn': 'pay', 'arg1': wallet, 'arg2': sum})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to pay ' + username

    # result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return 'ok'

def blockchain_user_newproject_request(username, projectName):
    result = __blockchain_request_raw('/blockchain/write', {'user': username, 'fcn': 'addProject', 'arg1': projectName.lower()})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to add project ' + projectName

    # result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return 'ok'

def blockchain_project_getbalance_request(username, pName):
    result = __blockchain_request_raw('/blockchain/read', {'user': username, 'fcn': 'query', 'arg1': pName})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to add project ' + username

    result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return result

def blockchain_user_getbalance_request(username, wallet):
    result = __blockchain_request_raw('/blockchain/read', {'user': username, 'fcn': 'query', 'arg1': wallet})
    if result.find('Error') > -1:
        return 'Fatal Error: Failed to get balance ' + username

    result = result.replace('success', '').replace("\r", '').replace("\n",'').strip()
    # result = json.loads(result)

    return result

def blockchain_project_status_request(username, pname):
    result = __blockchain_request_raw('/blockchain/read', {'user': username, 'fcn': 'query', 'arg1': pname.lower()})
    if result.find('Error') > -1:
        return 'Fatal Error: Failed to get status for project  ' + pname

    return 'ok'

def blockchain_user_getkey_request(username):
    result = __blockchain_request_raw('/blockchain/read', {'user': username, 'fcn': 'getKey'})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to get key user ' + username

    result = result.replace('success', '')

    return result


def blockchain_user_register_request(username):
    result = __blockchain_request_raw('/blockchain/register', {'user': username})
    if result.find('success') == -1:
        return 'Fatal Error: Failed to create user ' + username

    result = result.replace('success', '')

    return result


def server_request(project):
    result = __server_request_raw(project, '/container/start')
    if 'status' not in result or result['status'] != "OK":
        raise RuntimeError('Result is not acceptable')
    if 'mysql_password' in result and 'host' in result:
        AccessInterface.create_mysql_interface(password=result['mysql_password'], project=project, host=result['host'])
    return True


def __get_project_api_key(project):
    if not project.api_key:
        data = urllib.urlencode({'app_key': DOCKER_APP_KEY, 'project': project.repository})
        url = "http://" + DOCKER_HOST + "/container/key"
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.load(response)
        api_key = result['API_KEY']
        project.api_key = api_key
        project.save()
        return api_key
    return project.api_key


def __blockchain_request_raw(service_url, data):
    d = {'app_key': DOCKER_APP_KEY}
    for k in data:
        d[k] = data[k]
    data = urllib.urlencode(d)
    url = "http://" + DOCKER_HOST + service_url
    req = urllib2.Request(url, data)
    result = urllib2.urlopen(req)
    res = result.read()
    return res


def __server_request_raw(project, service_url):
    if not project.repository:
        raise AttributeError("repository for project is not found")
    api_key = __get_project_api_key(project)
    d = {'app_key': DOCKER_APP_KEY, 'project': project.repository, 'api_key': api_key}

    data = urllib.urlencode(d)
    url = "http://" + DOCKER_HOST + service_url
    req = urllib2.Request(url, data)
    result = urllib2.urlopen(req)

    result = json.load(result)

    return result


def server_status_request(project):
    result = __server_request_raw(project, '/container/status')
    if 'status' not in result or result['status'] != "UP":
        return False
    return True
