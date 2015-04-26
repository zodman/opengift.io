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
from PManager.viewsExt.projects import projectDetail, addInterface, removeInterface, checkUniqRepNameResponder
from PManager.viewsExt.file_view import docxView
from PManager.viewsExt.keys import KeyHandler
from robo.views import paysystems, payment
from PManager.xml_import.xml_import import XML_Import
from django.shortcuts import HttpResponse

admin.autodiscover()

from wiki.urls import get_pattern as get_wiki_pattern
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
    if sum == 900:
        user.is_staff = True
        user.save()
        date = profile.premium_till or datetime.datetime.now()
        date = date + datetime.timedelta(days=30)
        profile.premium_till = date
        profile.save()

        PM_Project.objects.filter(author=user, locked=True).update(locked=False)


result_received.connect(payment_received)


default_storage_uploader = AjaxFileUploader(backend=LocalUploadBackend)


def wikiCustomView(*args, **kwargs):
    wikiRealView = get_wiki_pattern()


urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', MainPage.indexRender,
                           {'widgetList': ["project_graph", "tasklist", "chat"], 'activeMenuItem': 'main'}),
                       url(r'^invite/$', MainPage.indexRender,
                           {
                               'widgetList': ["tasklist"],
                               'widgetParams': {
                                   'invite': True
                               }
                           }
                       ),
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
                       url(r'^milestones/$', milestonesResponder),
                       url(r'^files_ajax/$', ajaxFilesResponder),
                       url(r'^messages_ajax/$', messagesAjaxResponder),
                       url(r'^users_ajax/$', userHandlers.setUserOptions),
                       url(r'^user_key_handle/add/$', KeyHandler.key_add),
                       url(r'^user_key_handle/remove/(?P<key_id>[0-9_]+)', KeyHandler.key_remove),
                       url(r'^wiki/', get_wiki_pattern()),
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
                       # url(r'^tracker/', include('tracker.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *", mimetype="text/plain")),
                       # (r'^search/', include('haystack.urls')),
                       url(r'^robokassa/', include('robokassa.urls')),
                       url(r'^payment_info/', paysystems),
                       url(r'^payment/', payment),
                       url(r'^promo_tmp/', MainPage.promoTmp),
)
