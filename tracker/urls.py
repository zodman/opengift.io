from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from PManager.views import MainPage, Brains, add_timer
from PManager.viewsExt.git_view import GitView
from PManager.viewsExt.tasks import taskListAjax, ajaxNewTaskWizardResponder, microTaskAjax
from PManager.viewsExt.messages import ajaxResponder as messagesAjaxResponder
from PManager.viewsExt.files import fileSave, ajaxFilesResponder, AjaxFileUploader, DeleteUploadedFile
from PManager.viewsExt.setup import register, recall
from PManager.viewsExt.milestones import ajaxMilestonesResponder, milestonesResponder, milestoneForm
from PManager.viewsExt.users import userHandlers
from PManager.viewsExt.notice import noticeSetRead
from PManager.viewsExt.task_drafts import taskdraft_detail, taskdraft_task_discussion, \
    taskdraft_resend_invites, taskdraft_accept_developer
from PManager.viewsExt.projects import projectDetail, addInterface, removeInterface, checkUniqRepNameResponder, project_server_setup, project_server_status
from PManager.viewsExt.file_view import docxView
from PManager.viewsExt.keys import KeyHandler
from PManager.viewsExt.assets import protected_file
from PManager.viewsExt.sniffer import get_errors
from PManager.viewsExt.forms import sendFeedback
from PManager.viewsExt.specialty import specialty_ajax
from robo.views import paysystems, payment
from PManager.xml_import.xml_import import XML_Import
from django.shortcuts import HttpResponse


admin.autodiscover()

from django_notify.urls import get_pattern as get_notify_pattern

from ajaxuploader.backends.local import LocalUploadBackend
from robokassa.signals import result_received
from PManager.models.payments import Payment
from PManager.models.tasks import PM_Project
from django.contrib.auth.models import User
import datetime


def payment_received(sender, **kwargs):
    id = int(kwargs['extra']['user'])
    user = User.objects.get(id=id)
    # role = PM_ProjectRoles.objects.get(project=project, role__code='client')
    profile = user.get_profile()
    sum = int(float(kwargs['OutSum']))

    if sum:
        days = None
        if sum == 900:
            days = 30
        elif sum == 2300:
            days = 90
        elif sum == 9000:
            days = 365

        if days:
            user.is_staff = True
            user.save()
            date = profile.premium_till or datetime.datetime.now()
            date = date + datetime.timedelta(days=days)
            profile.premium_till = date
            profile.save()

        PM_Project.objects.filter(author=user, locked=True).update(locked=False)

result_received.connect(payment_received)

default_storage_uploader = AjaxFileUploader(backend=LocalUploadBackend)


urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', MainPage.indexRender,
                           {'widgetList': ["project_graph", "tasklist", "chat"], 'activeMenuItem': 'main'}),

                       url(r'^gantt/$', MainPage.indexRender, {'widgetList': ["gantt"], 'activeMenuItem': 'main'}),
                       url(r'^widgets/js/(?P<widget_name>[A-z_]+)/(?P<script_name>[A-z_\.]+)\.js', MainPage.jsWidgetProxy),
                       url(r'^widget_update/(?P<widget_name>[A-z_]+)', MainPage.widgetUpdate),
                       url(r'^user_list/', MainPage.indexRender, {'widgetList': ["user_list"]}),
                       url(r'^life/', MainPage.indexRender, {'widgetList': ["life"]}),
                       url(r'^achievements/', MainPage.indexRender, {'widgetList': ["achievements"]}),
                       url(r'^user_detail/', MainPage.indexRender, {'widgetList': ["user_detail"]}, name='user-detail'),
                       url(r'^task_edit/$', MainPage.indexRender,
                           {'widgetList': ["task_edit"], 'activeMenuItem': 'tasks'}),
                       url(r'^task_detail/$', MainPage.indexRender,
                           {'widgetList': ["task_detail"], 'activeMenuItem': 'tasks'}),
                       url(r'^task_handler', taskListAjax, name='task-handler'),
                       url(r'^sendfile/', fileSave),
                       url(r'^calendar/', MainPage.indexRender,
                           {'widgetList': ["project_calendar"], 'activeMenuItem': 'calendar'}),
                       url(r'^profile/edit/', MainPage.indexRender,
                           {'widgetList': ["profile_edit"], 'activeMenuItem': 'profile'}),
                       url(r'^project/(?P<project_id>[0-9_]+)/server-setup', project_server_setup),
                       url(r'^project/(?P<project_id>[0-9_]+)/server-status', project_server_status),
                       url(r'^project/(?P<project_id>[0-9_]+)', projectDetail),
                       url(r'^add_interface/', addInterface),
                       url(r'^remove_interface/', removeInterface),
                       url(r'^project/edit/check_repository_name', checkUniqRepNameResponder),
                       url(r'^commit/show', GitView.show_commit),
                       url(r'^project/edit/', MainPage.indexRender,
                           {'widgetList': ["project_edit"], 'activeMenuItem': 'project'}),
                       url(r'^upload/receiver$', default_storage_uploader, name="ajax-upload-default-storage"),
                       url(r'^upload/receiver/(?P<handler_id>[A-z0-9_\-]+)$', DeleteUploadedFile),
                       url(r'^files/$', MainPage.indexRender, {'widgetList': ["file_list"]}),
                       url(r'^new_task_wizard/$', ajaxNewTaskWizardResponder),
                       url(r'^milestone_ajax/$', ajaxMilestonesResponder),
                       url(r'^taskdrafts/$', MainPage.indexRender,
                           {'widgetList': ['taskdrafts'], 'activeMenuItem': 'main'}),
                       url(r'^taskdraft/(?P<draft_slug>[0-9A-z_]{64})/resend-invites$', taskdraft_resend_invites),
                       url(r'^taskdraft/(?P<draft_slug>[0-9A-z_]{64})/(?P<task_id>[0-9]+)/accept-developer$',
                           taskdraft_accept_developer),
                       url(r'^taskdraft/(?P<draft_slug>[0-9A-z_]{64})/(?P<task_id>[0-9]+)$', taskdraft_task_discussion),
                       url(r'^taskdraft/(?P<draft_slug>[0-9A-z_]{64})$', taskdraft_detail),
                       url(r'^milestones/$', milestonesResponder),
                       url(r'^files_ajax/$', ajaxFilesResponder),
                       url(r'^messages_ajax/$', messagesAjaxResponder),
                       url(r'^users_ajax/$', userHandlers.setUserOptions),
                       url(r'^user_key_handle/add/$', KeyHandler.key_add),
                       url(r'^user_key_handle/remove/(?P<key_id>[0-9_]+)', KeyHandler.key_remove),
                       url(r'^notify/', get_notify_pattern()),
                       url(r'^import_teamlab/', XML_Import.importView),
                       url(r'^statistic/$', MainPage.indexRender, {'widgetList': ["user_statistic"]}),
                       url(r'^stat/$', MainPage.indexRender, {'widgetList': ["project_statistic"]}),
                       url(r'^projects_summary/$', MainPage.indexRender, {'widgetList': ["project_summary"]}),
                       url(r'^register/$', register),
                       url(r'^phone_invite/$', recall),
                       url(r'^docx/$', docxView),
                       url(r'^train/$', Brains.trainTasksBrains),
                       url(r'^ajax/notice$', noticeSetRead),
                       url(r'^cost/$', MainPage.paymentReport),
                       url(r'^credits/$', MainPage.creditReport),
                       url(r'^credit_chart/$', MainPage.creditChart),
                       url(r'^login/$', MainPage.auth),
                       url(r'^add_timer/', add_timer),
                       url(r'^kanban/', MainPage.indexRender, {'widgetList': ["kanban"]}),
                       url(r'^ajax/micro_task/(?P<task_id>[0-9_]+)', microTaskAjax),
                       url(r'^ajax/responsible_menu/$', userHandlers.getResponsibleMenu),
                       url(r'^ajax/milestone_create/$', milestoneForm),
                       url(r'^ajax/feedback/$', sendFeedback),
                       url(r'^ajax/specialty/$', specialty_ajax),
                       url(r'^file_access/', protected_file),
                       url(r'^sniffer/get_errors/', get_errors),
                       # url(r'^tracker/', include('tracker.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\r\nDisallow: /static/\r\n", mimetype="text/plain")),
                       # (r'^search/', include('haystack.urls')),
                       url(r'^robokassa/', include('robokassa.urls')),
                       url(r'^payment_info/', paysystems),
                       url(r'^payment/', payment),
                       url(r'^promo_tmp/', MainPage.promoTmp),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf here ...

urlpatterns += staticfiles_urlpatterns()