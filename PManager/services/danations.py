__author__ = 'rayleigh'
from PManager.models.tasks import PM_Project_Donation
from django.contrib.auth.models import User


def donate(sum, project, user=None, milestone=None, exchangeUser=None, refUser=None):
    from PManager.services.docker import blockchain_donate_request
    if not project.blockchain_name:
        return False

    if user and user.is_authenticated() and user.get_profile().hasRole(project):
        return False

    milestoneCode = None
    if milestone:
        milestoneCode = 'opengift.io:' + str(milestone.id)
        milestone.is_request = False
        milestone.save()

    res = blockchain_donate_request(
        exchangeUser if exchangeUser else user.username,
        project.blockchain_name,
        sum,
        milestoneCode
    )

    if res == 'ok':
        if exchangeUser:
            try:
                exchangeUser = User.objects.get(username=exchangeUser)
            except User.DoesNotExist:
                pass

        donation = PM_Project_Donation(
            user=user,
            project=project,
            sum=sum,
            milestone=milestone,
            exchange=exchangeUser,
            ref=refUser
        )
        donation.save()
        return True

    return False
