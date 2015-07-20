__author__ = 'rayleigh'
from PManager.models.tasks import PM_Project


def get_project_by_id(project_id):
    try:
        project = PM_Project.objects.get(pk=int(project_id))
        return project
    except ValueError, PM_Project.DoesNotExist:
        return None
