# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from PManager.models.tasks import PM_Task, ObjectTags, PM_Task_Message
from django.db.models import Count

def similar_tasks(task_id, limit=4, tagsRelations=[]):
    aSimilarTasks = []
    try:
        task = PM_Task.objects.get(pk=int(task_id))
    except (PM_Task.DoesNotExist, ValueError, TypeError):
        return aSimilarTasks
    if not tagsRelations:
        tagsRelations = tags_relations(task)

    if tagsRelations:
        aTasksFromRelations = []
        for rel in tagsRelations:
            aTasksFromRelations.append(rel.object_id)
        aSimilarTasks = PM_Task.objects.filter(pk__in=aTasksFromRelations, project=task.project).exclude(
            id=task.id)[:limit]

    return aSimilarTasks

def tags_relations(task):
    tags = task.tags.all()
    return ObjectTags.objects.filter(tag__in=tags.values('tag')).annotate(
        dcount=Count('object_id')) if tags else []


def similar_solutions(task_id, limit=4):
    tasks = similar_tasks(task_id, limit)
    tasks_ids = set(task.id for task in tasks)
    aMessages = []
    try:
        messages = PM_Task_Message.objects.filter(task__in=tasks_ids, solution=True)
        for message in messages:
            aMessages.append(message)
        return aMessages
    except PM_Task_Message.DoesNotExist:
        return aMessages


