# -*- coding:utf-8 -*-
from PManager.models import PM_Task, PM_User, PM_Timer
from PManager.widgets.tasklist.widget import widget as taskList
from django.contrib.auth.models import User
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
__author__ = 'Gvammer'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


def widget(request, headerValues, ar, qargs):
    if request.user.is_superuser:
        class ProfileForm(forms.ModelForm):
            class Meta:
                model = PM_User
                fields = ['second_name', 'phoneNumber', 'skype', 'avatar', 'specialties', 'hoursQtyPerDay',  'sp_price', 'overdraft', 'documentNumber', 'documentIssueDate', 'documentIssuedBy', 'order', 'bik', 'bank']
    else:
        class ProfileForm(forms.ModelForm):
            class Meta:
                model = PM_User
                fields = ['second_name', 'phoneNumber', 'skype', 'avatar', 'hoursQtyPerDay', 'documentNumber', 'documentIssueDate', 'documentIssuedBy', 'order', 'bik', 'bank']

    uid = request.GET.get('id', None)
    if uid and request.user.is_staff:
        user = User.objects.get(pk=uid)
    else:
        user = request.user

    profile = user.get_profile()
    avatarUrl = profile.avatar
    c = RequestContext(request, processors=[csrf])

    if request.method == 'POST': # If the form has been submitted...

        form = ProfileForm(instance=profile, data=request.POST,
                           files=request.FILES) # A form bound to the POST data
        uform = UserForm(instance=user, data=request.POST, files=request.FILES) # A form bound to the POST data
        if form.is_valid() and uform.is_valid(): # All validation rules pass
            form.save()
            uform.save()

            password = request.POST.get('new_password', None)
            if password:
                password_confirm = request.POST.get('new_password_confirm', None)
                if password_confirm == password:
                    user.set_password(password_confirm)
                    user.save()

            return {'redirect': '/profile/edit/?id='+str(uid)}
    else:
        form = ProfileForm(instance=profile) # An unbound form
        uform = UserForm(instance=user) # An unbound form

    try:
        if profile.avatar:
            profile.avatar = str(profile.avatar).replace('PManager', '')

        timers = PM_Timer.objects.raw(
            'SELECT SUM(`seconds`) as summ, id, user_id from PManager_pm_timer WHERE `user_id`=' + str(int(user.id)))
        sum = 0
        if timers:
            for timer in timers:
                if timer.summ:
                    sum += float("%.2f" % (float(timer.summ) / 3600))

        setattr(profile, 'sp', {
            'summ': sum,
            'rest': sum * int(profile.sp_price) if profile.sp_price else 0
        })

    except User.DoesNotExist:
        pass

    return {
        'c': c,
        'user': user,
        'profile': profile,
        'form': form,
        'uform': uform,
        'title': u'Редактирование профиля'
    }