# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.template import loader, RequestContext
from PManager.models import PM_Task, PM_Project, PM_Achievement, SlackIntegration, ObjectTags, PM_Timer
from PManager.models import LikesHits, PM_Project_Problem, RatingHits, PM_Project_Achievement, PM_ProjectRoles, PM_Milestone, PM_Files
from PManager.models import AccessInterface, Credit, PM_Project_Industry
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from PManager.classes.language.translit import transliterate
from tracker.settings import USE_GIT_MODULE, COMISSION
from PManager.viewsExt.headers import set_project_in_session
from django.contrib.contenttypes.models import ContentType
from PManager.classes.git.gitolite_manager import GitoliteManager
import json, math, random
from django.core.context_processors import csrf
from django.db.models import Sum
from PManager.viewsExt.tools import templateTools

class InterfaceForm(forms.ModelForm):
    class Meta:
        model = AccessInterface
        fields = ["name", "address", "port", "protocol",
                  "username", "password", "access_roles", "project"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = PM_Project
        fields = ["name", "description", "author", "tracker"]
        if USE_GIT_MODULE:
            fields.append("repository")

    def clean_repository(self):
        if USE_GIT_MODULE:
            return self.cleaned_data['repository'].strip()


class ProjectFormEdit(forms.ModelForm):
    class Meta:
        model = PM_Project
        fields = ["name", "share_link_enabled", "description", "public", "files", "industries", "target_group", "problem", "link_site", "link_github", "link_video", "link_demo"]
        if USE_GIT_MODULE:
            fields.append("repository")

def getIndustriesTree():
    specialties = PM_Project_Industry.objects.filter()
    aSpecialties = {}

    for spec in specialties:
        aSpecialties[spec.id] = {
            'item': spec,
            'subitems': []
        }

    aSpecialtiesTree = []

    for key, spec in aSpecialties.iteritems():
        s = spec['item']
        if s.parent:
            if aSpecialties[s.parent.id] and aSpecialties[s.id]:
                aSpecialties[s.parent.id]['subitems'].append(aSpecialties[s.id])
                aSpecialtiesTree.append(s.id)

    for id in aSpecialtiesTree:
        del aSpecialties[id]


    return aSpecialties

def projectList(request, **kwargs):
    aSpec = getIndustriesTree()

    def recursiveTreeDraw(treeItem):
        s = ''
        if 'item' in treeItem:
            s += '{value:25, label: "'
            s += treeItem['item'].name
            s += '", subitems: ['

        if treeItem['subitems']:
            for item in treeItem['subitems']:
                s += recursiveTreeDraw(item)

        if 'item' in treeItem:
            s += ']},'

        return s

    c = RequestContext(request, {
        'specialties': aSpec,
        'spectree': recursiveTreeDraw({'subitems': aSpec.values()}),
        'project_list': PM_Project.objects.filter(public=True).order_by('-id')
    })
    c.update(kwargs)
    t = loader.get_template('details/project_list.html')
    return HttpResponse(t.render(c))

def projectDetailDonate(request, project_id):

    project = get_object_or_404(PM_Project, id=project_id)
    milestoneId = request.GET.get('m', None)
    milestone = None
    if milestoneId:
        try:
            milestone = project.milestones.get(pk=int(milestoneId))
        except PM_Milestone.DoesNotExist:
            pass

    c = RequestContext(request, {
        'project': project,
        'milestone': milestone
    })

    t = loader.get_template('details/project_donate.html')
    return HttpResponse(t.render(c))

def projectDetailEdit(request, project_id):
    project = get_object_or_404(PM_Project, id=project_id)
    if not request.user.is_authenticated() or not request.user.get_profile().isManager(project):
        raise Http404

    if request.method == 'POST':
        p_form = ProjectFormEdit(
            data=request.POST,
            files=request.FILES,
            instance=project
        )
        if p_form.is_valid():
            p_form.save()

            iter = project.files.count()
            for file in request.FILES.getlist('IMAGES'):
                iter = iter + 1
                f = PM_Files(
                    name=project.name + str(iter),
                    file=file,
                    authorId=request.user,
                    projectId=project
                )
                f.save()
                project.files.add(f)

            for m in project.milestones.filter(closed=False):
                name = request.POST.get('milestone_'+str(m.id)+'_name', None)
                if name:
                    m.name = name
                    m.date = templateTools.dateTime.convertToDateTime(request.POST.get('milestone_'+str(m.id)+'_date', ''))
                    m.description = request.POST.get('milestone_'+str(m.id)+'_desc', '')
                    m.save()
                else:
                    m.delete()

            new_milestones = request.POST.getlist('milestone_new_name')
            new_milestones_date = request.POST.getlist('milestone_new_date')
            new_milestones_desc = request.POST.getlist('milestone_new_desc')
            i = 0
            for ms_name in new_milestones:
                if ms_name:
                    ms_date = templateTools.dateTime.convertToDateTime(new_milestones_date[i])
                    ms = PM_Milestone(
                        name=ms_name,
                        description=new_milestones_desc[i],
                        date=ms_date,
                        project=project,
                        author=request.user
                    )
                    ms.save()
                i += 1

            for m in project.problems.all():
                name = request.POST.get('problem_'+str(m.id)+'_problem', None)
                if name:
                    m.problem = name
                    m.target_group = request.POST.get('problem_'+str(m.id)+'_target_group', '')
                    m.solution = request.POST.get('problem_'+str(m.id)+'_solution', '')
                    m.save()
                else:
                    project.problems.remove(m)

            new_problems = request.POST.getlist('problem_new_problem')
            new_problems_target_group = request.POST.getlist('problem_new_target_group')
            new_problems_solution = request.POST.getlist('problem_new_solution')
            i = 0
            for ms_name in new_problems:
                if ms_name:
                    try:
                        ms = PM_Project_Problem.objects.get(
                            problem=ms_name,
                            target_group=new_problems_target_group[i],
                        )
                    except PM_Project_Problem.DoesNotExist:
                        ms = PM_Project_Problem(
                            problem=ms_name,
                            target_group=new_problems_target_group[i],
                            solution=new_problems_solution[i]
                        )

                    ms.save()
                    project.problems.add(ms)

                i += 1


            return HttpResponse('ok')
        else:
            return HttpResponse(p_form.errors)

    aSpecialties = getIndustriesTree()

    sprojectSpec = project.industries.values_list('id', flat=True)

    def recursiveTreeDraw(treeItem):
        s = ''
        if 'item' in treeItem:
            percent = str(treeItem['item'].getPercent())
            s += '<li class="js-section-item project-form--specialties-container-ul-li">'
            s += '<div class="progress-item">'
            s += '<label class="custom-control custom-checkbox text-left"><input '+(
                'checked ' if treeItem['item'].id in sprojectSpec else '')+' type="checkbox" name="industries" value="' + str(
                treeItem['item'].id) + '" class="custom-control-input"><span class="custom-control-indicator mt-1"></span>'
            s += '<span class="custom-control-description">'+treeItem['item'].name+'</span>'
            s += '</label>'
            if treeItem['subitems']:
                s += '<div class="js-toggle-section float-right up-down-icon"><i class="fa fa-angle-down"></i></div>'
            s += '<h4 class="float-right text-primary">'+percent+'%</h4>'
            s += '<div class="progress w-100">'
            s += '<div class="progress-bar" aria-valuenow="'+percent+'" style="width: '+percent+'%;"></div>'
            s += '</div>'

            s += '</div>'

        if treeItem['subitems']:

            s += '<ul class="project-form--specialties-container-ul js-subitems-list" '+('style="display:none;"' if 'item' in treeItem else '')+'>'
            for item in treeItem['subitems']:
                s += recursiveTreeDraw(item)

            if 'item' in treeItem:
                curId = treeItem['item'].id
                s += '<li class="project-form--specialties-container-ul-li-ul-li js-add-item">'
                s += '<div class="progress-item">'
                s += '<div class="row">'
                s += '<div class="col-md-6 u-mb-30">'
                s += u'<input type="text" class="input-sm js-category-name" placeholder="Add your option..." />'
                s += '</div>'
                s += '<div class="col-md-6 u-mb-30">'
                s += u'<button data-id="'+str(curId)+u'" class="js-add-category-btn btn btn-primary btn-sm"> Add</button>'
                s += '</div>'
                s += '</div>'
                s += '</div>'
                s += '</li>'
            s += '</ul>'

        if 'item' in treeItem:
            s += '</li>'

        return s

    c = RequestContext(request, {
        'milestones': project.milestones.filter(closed=False, donated=False).order_by('date'),
        'project': project,
        'e': sprojectSpec,
        'industries': aSpecialties,
        'industriesList': recursiveTreeDraw({'subitems': aSpecialties.values()})
    })

    t = loader.get_template('details/project_edit.html')
    return HttpResponse(t.render(c))


def projectDetailAjax(request, project_id):
    project = get_object_or_404(PM_Project, id=project_id)
    canDeleteProject, canEditProject, bCurUserIsAuthor = False, False, False
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        canDeleteProject = request.user.is_superuser or request.user.id == project.author.id
        canEditProject = request.user.is_superuser or request.user.id == project.author.id
        bCurUserIsAuthor = request.user.id == project.author.id or profile.isManager(project)

    action = request.POST.get('action')
    if action == 'rate':
        if not RatingHits.userVoted(project, request):
            rating = int(request.POST.get('rating'))
            if (rating > 5): rating = 5
            rateObject = RatingHits(project=project, rating=rating)
            rateObject.save(request=request)
    elif action == 'like':
        mid = int(request.POST.get('mid'))
        milestone = get_object_or_404(PM_Milestone, id=mid)
        if not LikesHits.userLiked(milestone, request):
            likeObject = LikesHits(milestone=milestone)
            likeObject.save(request=request)

    elif action == 'addProblem':
        name = request.POST.get('name', '')
        parent = int(request.POST.get('parent', 0))
        if not name:
            return HttpResponse('Insert name')

        try:
            industry = PM_Project_Industry.objects.get(name=name)
            return HttpResponse('Industry already exists')
        except PM_Project_Industry.DoesNotExist:
            try:
                parent = PM_Project_Industry.objects.get(pk=parent)
                industry = PM_Project_Industry(name=name, parent=parent)
                industry.save()
                return HttpResponse(industry.id)
            except PM_Project_Industry.DoesNotExist:
                return HttpResponse('Empty parent')

    elif action == 'milestones':
        milestones = PM_Milestone.objects.filter(project=project, closed=False).order_by('date')
        a = []
        for milestone in milestones:
            a.append({
                'id': milestone.id,
                'name': milestone.name.replace('script', 'sc ript'),
                'description': milestone.description.replace('script', 'sc ript'),
                'date': milestone.date.strftime('%d.%m.%Y') if milestone.date else '',
                'likesQty': milestone.likesHits.count(),
                'donationsQty': milestone.donations.count(),
                'percent': milestone.percent()
            })

        return HttpResponse(json.dumps(a))

    return HttpResponse('ok')

def projectDetailAdd(request):
    import urllib
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?backurl='+urllib.quote(request.get_full_path()))

    post = request.POST if request.method == 'POST' else {}

    p_form = ProjectForm(
        data=post,
        files=request.FILES
    )

    instance = None
    if request.method == 'POST':
        if not request.user.is_authenticated():
            raise Http404

        if request.user.createdProjects.exists():
            raise Http404

        post.update({'author': request.user.id})
        post.update({'tracker': 1})

        if p_form.is_valid():
            instance = p_form.save()
            iter = 0
            for file in request.FILES.getlist('IMAGES'):
                iter = iter + 1
                f = PM_Files(
                    name=instance.name + str(iter),
                    file=file,
                    authorId=request.user,
                    projectId=instance
                )
                f.save()
                instance.files.add(f)

            instance.public = True
            instance.save()

            request.user.get_profile().setRole('manager', instance)
            return HttpResponseRedirect('/project/' + str(instance.id) + '/edit/')

    c = RequestContext(request, {
        'form': p_form,
        'instance': instance,
        'register': True if request.GET.get('register', None) == 'yes' else False
    }, processors=[csrf])

    t = loader.get_template('details/project_add.html')
    return HttpResponse(t.render(c))


def projectDetailPublic(request, project_id):
    import datetime
    from PManager.widgets.project_statistic import widget as stat_widget

    project = get_object_or_404(PM_Project, id=project_id)
    canDeleteProject, canEditProject, bCurUserIsAuthor = False, False, False
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        canDeleteProject = request.user.is_superuser or request.user.id == project.author.id
        canEditProject = request.user.is_superuser or request.user.id == project.author.id
        bCurUserIsAuthor = request.user.id == project.author.id or profile.isManager(project)

    if request.POST.get('invest_offer', None):
        from PManager.viewsExt.tools import emailMessage
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'tokens': request.POST.get('tokens'),
            'offer': request.POST.get('offer'),
            'project': project.name,
        }

        sendMes = emailMessage(
            'new_investment_request', data, 'New investment request')

        try:
            sendMes.send(['gvamm3r@gmail.com'])
        except Exception:
            print 'Message is not sent'

        return HttpResponseRedirect(request.get_full_path())

    projectSettings = project.getSettings()
    daysBeforeNowForStartFilt = 7
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())

    dateFrom = now - datetime.timedelta(days=daysBeforeNowForStartFilt)

    dateTo = now

    dayGenerator = [dateFrom + datetime.timedelta(x + 1) for x in
                    xrange((dateTo - dateFrom).days)]

    xAxe = []
    yAxes = {
        u'Задачи': {
            'title': u'Задачи',
            'color': 'rgba(54, 162, 235, 1)',
            'values': []
        },
        u'Коммиты': {
            'title': u'Коммиты',
            'color': 'rgba(255,99,132,1)',
            'values': []
        }
    }

    for day in dayGenerator:
        yAxes[u'Задачи']['values'].append(random.randint(1, 27))
        yAxes[u'Коммиты']['values'].append(random.randint(1, 27))
        xAxe.append(day)

    statistic = stat_widget(request, {'getAllCharts': 1, 'CURRENT_PROJECT': project}, None, None)

    team = []

    for user in project.getUsers():
        taskTagCoefficient = 0
        for obj1 in ObjectTags.objects.raw(
                                                'SELECT SUM(`weight`) as weight_sum, `id` from PManager_objecttags WHERE object_id=' + str(
                                            user.id) + ' AND content_type_id=' + str(
                            ContentType.objects.get_for_model(User).id) + ''):
            taskTagCoefficient += (obj1.weight_sum or 0)
            break

        setattr(user, 'rating', taskTagCoefficient)
        team.append(user)

    ms = PM_Milestone.objects.filter(project=project).order_by('date')
    ams = []
    for m in ms:
        setattr(m, 'liked', m.userLiked(request))
        ams.append(m)

    timers = PM_Timer.objects.raw(
            'SELECT SUM(`seconds`) as summ, id from PManager_pm_timer' +
            ' WHERE `task_id` IN (select id from PManager_pm_task where closed=1 and project_id=' + str(project.id) + ')'
        )
    time = 0
    for t in timers:
        if t.summ:
            time += float(t.summ)

    time /= 3600
    time = round(time)

    aIndustries = [p for p in project.industries.filter(active=True)]
    project.link_video = project.link_video.replace("watch?v=", "embed/")
    c = RequestContext(request, {
        'chart': {
            'xAxe': xAxe,
            'yAxes': yAxes,
        },
        'statistic': statistic,
        'tagList': aIndustries,
        'donationsCount': project.donations.count(),
        'project': project,
        'milestones': ams,
        'team': team,
        'hours_spent': time,
        'canDelete': canDeleteProject,
        'canEdit': canEditProject,
        'bCurUserIsAuthor': bCurUserIsAuthor,
        'settings': projectSettings,
        'long_industries_list': len(aIndustries) > 3,
        'raters_count': project.votersQty,
        'user_voted': RatingHits.userVoted(project, request),
        'rating': project.rating
    })
    if request.GET.get('frame'):
        t = loader.get_template('details/project_widget.html')
    else:
        t = loader.get_template('details/project_pub.html')
    response = HttpResponse(t.render(c))

    from PManager.viewsExt.tools import set_cookie
    if request.GET.get('ref'):
        set_cookie(response, 'ref', request.GET.get('ref'))

    return response


def projectDetailServer(request, project_id):
    project = get_object_or_404(PM_Project, id=project_id)
    profile = request.user.get_profile()
    canDeleteProject = request.user.is_superuser or request.user.id == project.author.id
    canEditProject = request.user.is_superuser or request.user.id == project.author.id
    bCurUserIsAuthor = request.user.id == project.author.id or profile.isManager(project)
    projectSettings = project.getSettings()

    c = RequestContext(request, {
        'project': project,
        'canDelete': canDeleteProject,
        'canEdit': canEditProject,
        'bCurUserIsAuthor': bCurUserIsAuthor,
        'settings': projectSettings,
        'activeMenuItem': 'server'
    })

    t = loader.get_template('details/project_server.html')
    return HttpResponse(t.render(c))


def projectDetail(request, project_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    project = get_object_or_404(PM_Project, id=project_id)
    profile = request.user.get_profile()

    if not profile.hasRole(project) or project.locked:
        raise Http404('Project not found')

    set_project_in_session(project.id, [project.id], request)
    aMessages = {
        'client': u'Бонусы за каждый час закрытых задач списываются с клиента, у которого установлена ставка.',
        'manager': u'Менеджеры проектов видят все задачи и имеют возможность изменять настройки проекта.',
        'employee': u'Сотрудники проектов видят только свои задачи или задачи, в которые их пригласили в качестве наблюдателей.',
        'guest': u'Гости могут видеть только задачи, в которых они назначены наблюдателями, в переписке гости видят только адресованные им сообщения.',
    }
    show = dict(manager=True)
    show['employee'] = profile.isManager(project) or profile.isEmployee(project)
    show['client'] = profile.isManager(project) or profile.isClient(project)
    show['guest'] = profile.isManager(project)

    needComission = profile.isManager(project) or profile.isClient(project)

    aDebts = Credit.getUsersDebt([project])
    oDebts = dict()
    for x in aDebts:
        oDebts[x['user_id']] = int(x['sum'])

    aRoles = dict()

    for role in PM_ProjectRoles.objects.filter(project=project, user__is_active=True):
        if not show[role.role.code]:
            continue

        if role.role.name not in aRoles:
            aRoles[role.role.name] = dict(role=role, users=[], text=aMessages[role.role.code])

        prof = role.user.get_profile()
        curUser = role.user

        rate = int(math.floor(role.rate or prof.sp_price or 0))
        if needComission:
            clientComission = int(project.getSettings().get('client_comission', 0) or COMISSION)
            rate = int(math.floor(rate * (clientComission + 100) / 100))

        setattr(curUser, 'rate', rate)
        setattr(curUser, 'payment_type', role.payment_type)
        # setattr(curUser, 'defaultRate', prof.sp_price)
        setattr(curUser, 'sum', oDebts.get(role.user.id, None))
        setattr(curUser, 'role_id', role.id)

        aRoles[role.role.name]['users'].append(curUser)

    bCurUserIsAuthor = request.user.id == project.author.id or profile.isManager(project)
    if bCurUserIsAuthor:
        action = request.POST.get('action', None)
        if action:
            role_id = request.POST.get('role')
            role = None
            responseObj = {}
            try:
                role = PM_ProjectRoles.objects.get(pk=role_id, project=project)
            except PM_ProjectRoles.DoesNotExist:
                responseObj = {'error': 'Something is wrong  :-('}

            if action == 'update_payment_type':
                if role:
                    type = 'real_time' if request.POST.get('value', '') == 'real_time' else 'plan_time'
                    role.payment_type = type
                    role.save()
                    responseObj = {'result': 'payment type updated'}

            elif action == 'update_rate':
                if role:
                    rate = int(request.POST.get('value', 0))
                    role.rate = rate
                    role.save()
                    responseObj = {'result': 'rate updated'}

            elif action == 'remove_role':
                if role:
                    res = role.safeDelete()
                    if res:
                        responseObj = {'result': 'role removed'}
                    else:
                        responseObj = {'error': u'Вы не можете удалить последнюю роль менеджера в проекте'}

            elif action == 'send_payment':
                if role:
                    sum = int(request.POST.get('sum', 0))
                    comment = request.POST.get('comment', '')
                    p = Credit(user=role.user, project=project, value=sum, type='payment', comment=comment)
                    p.save()

                    responseObj = {'result': 'payment added'}

            elif action == 'change_name':
                if 'name' in request.POST:
                    project.name = request.POST['name']
                elif 'description' in request.POST:
                    project.description = request.POST['description']
                elif 'file' in request.FILES:
                    project.image = request.FILES['file']

                project.save()

                responseObj = {'result': 'ok'}

            elif action == 'upload_project_avatar':
                image = request.FILES.get('image')
                project.image = image
                project.save()
                responseObj = {'path': project.image.url}

            elif action == 'update_achievement_exist':
                if 'achievement' in request.POST:
                    try:
                        ac = PM_Achievement.objects.get(pk=int(request.POST['achievement']))
                        exist = int(request.POST.get('value', False))
                        if exist:
                            PM_Project_Achievement.get_or_create(achievement=ac, project=project)
                        else:
                            pac = PM_Project_Achievement.objects.filter(achievement=ac, project=project)
                            pac.delete()

                        responseObj = {'result': 'ok'}
                    except PM_Achievement.DoesNotExist, PM_Project_Achievement.DoesNotExist:
                        responseObj = {'error': 'Achievement does not exist'}

            elif action == 'update_achievement_value':
                if 'achievement' in request.POST:
                    try:
                        ac = PM_Achievement.objects.get(pk=int(request.POST['achievement']))

                        pac, created = PM_Project_Achievement.get_or_create(achievement=ac, project=project)
                        pac.value = int(request.POST.get('value', 0))
                        pac.save()

                        responseObj = {'result': 'ok'}
                    except PM_Achievement.DoesNotExist:
                        responseObj = {'error': 'Achievement does not exist'}

            elif action == 'update_achievement_type':
                if 'achievement' in request.POST:
                    try:
                        ac = PM_Achievement.objects.get(pk=int(request.POST['achievement']))

                        pac, created = PM_Project_Achievement.get_or_create(achievement=ac, project=project)
                        pac.type = request.POST.get('value', 'fix')
                        pac.save()

                        responseObj = {'result': 'ok'}
                    except PM_Achievement.DoesNotExist:
                        responseObj = {'error': 'Achievement does not exist'}

            return HttpResponse(json.dumps(responseObj))

    canDeleteInterface = profile.isManager(project)
    canDeleteProject = request.user.is_superuser or request.user.id == project.author.id
    canEditProject = request.user.is_superuser or request.user.id == project.author.id

    try:
        s = SlackIntegration.objects.get(project=project)
        setattr(project, 'slackUrl', s.url)
    except SlackIntegration.DoesNotExist:
        setattr(project, 'slackUrl', '')

    if 'settings_save' in request.POST and request.POST['settings_save'] and canEditProject:
        if 'is_closed' in request.POST \
                and (bool(request.POST['is_closed']) != project.closed) \
                and canDeleteProject:
            project.closed = bool(request.POST['is_closed'])

        parseSettingsFromPost(project, request)
        project.save()
        return HttpResponseRedirect(request.path)

    if 'integration_settings_save' in request.POST and request.POST['integration_settings_save'] and canEditProject:
        if 'repository' in request.POST and request.POST['repository'] != project.repository:
            project.repository = request.POST['repository']

        parseSettingsFromPost(project, request)
        project.save()
        return HttpResponseRedirect(request.path)

    if 'integration_messangers_settings_save' in request.POST \
            and request.POST['integration_messangers_settings_save'] and canEditProject:
        if 'slack_url' in request.POST and request.POST['slack_url'] != project.slackUrl:
            try:
                s = SlackIntegration.objects.get(project=project)
            except SlackIntegration.DoesNotExist:
                s = SlackIntegration(project=project)

            s.url = request.POST['slack_url']
            s.save()
            setattr(project, 'slackUrl', s.url)

        return HttpResponseRedirect(request.path)

    interfaces = AccessInterface.objects.filter(project=project)
    interfaces_html = ''
    t = loader.get_template('details/interface.html')
    for interface in interfaces:
        c = RequestContext(request, {
            'interface': interface,
            'canDelete': canDeleteInterface,
            'show_git': USE_GIT_MODULE
        })

        interfaces_html += t.render(c)

    achievements = PM_Achievement.objects.filter(use_in_projects=True)
    ar_achievements = []
    ar_project_achievements = {}
    for p_ac in PM_Project_Achievement.objects.filter(project=project).select_related('achievement'):
        ar_project_achievements[p_ac.achievement.id] = p_ac

    for achievement in achievements:
        if achievement.id in ar_project_achievements:
            setattr(achievement, 'project_relation', ar_project_achievements[achievement.id])

        ar_achievements.append(achievement)

    projectSettings = project.getSettings()
    c = RequestContext(request, {
        'project': project,
        'pageTitle': project.name,
        'roles': aRoles,
        'form': InterfaceForm(),
        'interfaces': interfaces_html,
        'canDelete': canDeleteProject,
        'canEdit': canEditProject,
        'bCurUserIsAuthor': bCurUserIsAuthor,
        'messages': aMessages,
        'settings': projectSettings,
        'achievements': ar_achievements,
        'colors': [(code, projectSettings.get('color_name_' + code, '')) for code, color in PM_Task.colors]
    })

    t = loader.get_template('details/project.html')
    return HttpResponse(t.render(c))


def parseSettingsFromPost(project, request):
    settings = project.getSettings()

    for k, v in request.POST.iteritems():
        if k.find('settings_') > -1:
            k = k.replace('settings_', '')
            settings[k] = False if v == 'N' else v

    project.setSettings(settings)


def addInterface(request):
    post = request.POST
    try:
        project_id = int(post['pid'])
        project = PM_Project.objects.get(id=project_id)
        if request.user.get_profile().hasRole(project):
            post['project'] = project.id
            form = InterfaceForm(data=post)
            if form.is_valid():
                instance = form.save()
                return render(request, 'details/interface.html', {
                    'interface': instance
                })
    except PM_Project.DoesNotExist:
        pass

    return HttpResponse('Invalid form')


def removeInterface(request):
    interface = get_object_or_404(AccessInterface, id=int(request.POST['id']))
    if request.user.get_profile().isManager(interface.project):
        interface.delete()

    return HttpResponse('ok')


def checkUniqRepNameResponder(request):
    if not USE_GIT_MODULE:
        return HttpResponse("ERROR")

    name = request.POST.get('repoName', '')
    if not name or name == 'gitolite-admin':
        return HttpResponse("ERROR")
    name = transliterate(name)
    proj = PM_Project.objects.filter(repository=name)
    if (proj):
        reponame = GitoliteManager.get_suggested_name(name)
        if not reponame:
            return HttpResponse("ERROR")
        return HttpResponse(reponame)
    return HttpResponse(name)


def project_server_setup(request, project_id):
    if not project_id:
        raise Http404
    try:
        from PManager.services.docker import server_request
        project = PM_Project.objects.get(pk=project_id)
        server_request(project)
        return HttpResponse("OK")
    except (PM_Project.DoesNotExist, RuntimeError, AttributeError):
        raise Http404


def project_server_status(request, project_id):
    if not project_id:
        raise Http404
    try:
        from PManager.services.docker import server_status_request
        project = PM_Project.objects.get(pk=project_id)
        status = server_status_request(project)
        if status:
            return HttpResponse("OK")
        else:
            return HttpResponse("ERROR")
    except (PM_Project.DoesNotExist, RuntimeError, AttributeError):
        raise Http404
