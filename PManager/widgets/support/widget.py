# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.widgets.tasklist.widget import widget as taskList


def widget(request, headerValues, widgetParams={}, qArgs=[]):
    taskResult = taskList(request, headerValues, widgetParams, qArgs)

    return {'tasks':taskResult['tasks'],'users':taskResult['users']}