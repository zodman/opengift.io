# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.viewsExt.tools import templateTools
from PManager.models import Payment, Credit, PM_Project, PM_Timer
from django.db import connection
from django.contrib.auth.models import User

import datetime
from django.utils import timezone

class Axis:
    title = ''
    color = 'rgb(0,0,0)'
    values = []

    def __init__(self, title, color):
        self.title = title
        self.color = color
        self.values = []

class Chart:
    title = ''
    type = 'chart'
    #or table
    dateFrom = datetime.datetime
    dateTo = datetime.datetime
    projects = []
    xAxe = []
    yAxes = []

    def __init__(self, dateFrom, dateTo, projects):
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.projects = projects
        self.getData()

class simpleChart(Chart):
    title = u'Общая маржинальность'
    type = 'simple'
    def getData(self):
        cursor = connection.cursor()
        projects = '(' + ','.join([str(s.id) for s in self.projects]) + ')'
        qText = """
                  SELECT
                      sum(IF (`payer_id` IS NOT NULL, value, value * -1)) as summ
                      FROM pmanager_credit
                      WHERE project_id IN """ + projects + """
              """

        cursor.execute(qText)
        self.value = 0
        for x in cursor.fetchall():
            self.value += x[0]

class PaymentChart(Chart):
    title = u'Расчетная статистика'
    type = 'chart'
    payQuery = ''
    def getData(self):
        self.dayGenerator = [self.dateFrom + datetime.timedelta(x + 1) for x in xrange((self.dateTo - self.dateFrom).days)]
        aSums = []
        sOut = 0
        sIn = 0
        pIn = 0
        pOut = 0
        self.xAxe = []
        self.yAxes = {
            'in': Axis(u'Бонусов списано', '#0bd145'),
            'out': Axis(u'Бонусов начислено', '#003060'),
            # 'pin': Axis(u'Входящие платежи', 'rgba(63, 255, 0, 0.34)'),
            'pout': Axis(u'Погасили бонусов', 'rgba(0, 255, 232, 0.34)'),
        }

        def dateToDb(date, type):
            if type is 'max' or type is 'min':
                date = datetime.datetime.combine(date, getattr(datetime.time, type))

            strDate = templateTools.dateTime.convertToDb(date)

            return strDate #'STR_TO_DATE(\''+strDate+'\', \'%Y-%m-%d %H:%i:%s\')' if strDate else None

        paymentsIn = []
        paymentsOut = []
        creditsIn = []
        creditsOut = []

        dateMin = dateToDb(self.dateFrom, 'min')
        dateMax = dateToDb(self.dateTo, 'max')
        cursor = connection.cursor()

        q = """SELECT id, sum(`value`) as sum, date(`date`) as day FROM pmanager_payment WHERE
            `payer_id` IS NOT NULL AND `date` BETWEEN %s AND %s GROUP BY %s"""

        cursor.execute(q, [dateMin, dateMax, 'day'])

        for x in cursor.fetchall():
            paymentsIn.append(x)

        for day in self.dayGenerator:
            credit = Credit.objects.filter(
                date__range=(datetime.datetime.combine(day, datetime.time.min),
                             datetime.datetime.combine(day, datetime.time.max))
            )
            if self.projects:
                credit = credit.filter(project__in=self.projects)

            creditOut = credit.filter(user__isnull=False)
            creditIn = credit.filter(payer__isnull=False)

            sOut += sum(c.value for c in creditOut)
            sIn += sum(c.value for c in creditIn)


            payments = Payment.objects.filter(date__range=(datetime.datetime.combine(day, datetime.time.min),
                                                           datetime.datetime.combine(day, datetime.time.max)))
            if self.projects:
                payments = payments.filter(project__in=self.projects)

            paymentsOut = payments.filter(user__isnull=False)
            paymentsIn = payments.filter(payer__isnull=False)
            pOut += sum(c.value for c in paymentsOut)
            pIn += sum(c.value for c in paymentsIn)

            self.xAxe.append(day)
            self.yAxes['in'].values.append(sIn)
            self.yAxes['out'].values.append(sOut)
            # self.yAxes['pin'].values.append(pIn)
            self.yAxes['pout'].values.append(pOut)

class sumLoanChart(Chart):
    title = u'Текущие бонусы'
    type = 'table'
    def getData(self):
        arDebts = Credit.getUsersDebt(self.projects)

        self.cols = [
            {
                'name': u'ФИО'
            },
            {
                'name': u'Сумма'
            }
        ]
        self.rows = []
        for x in arDebts:
            try:
                user = User.objects.get(pk=int(x['user_id']))
                if x['sum']:
                    self.rows.append({
                        'cols': [
                            {
                                'url': '/user_detail/?id='+str(x['user_id']),
                                'text': user.last_name + ' ' + user.first_name
                            },
                            {
                                'text': x['sum']
                            }
                        ]
                    })
            except User.DoesNotExist:
                pass

class timeChart(Chart):
    title = u'Потраченное время'
    type = 'table'
    def getData(self):
        from django.db.models import Sum
        aTimers = PM_Timer.objects.filter(task__project__in=self.projects, dateEnd__range=(self.dateFrom, self.dateTo))\
            .values('user') \
                .annotate(score = Sum('seconds'))


        self.cols = [
            {
                'name': u'ФИО'
            },
            {
                'name': u'Потрачено времени'
            },
            {
                'name': u'Закрыто по плану'
            }
        ]
        self.rows = []
        for x in aTimers:
            try:
                user = User.objects.get(pk=int(x['user']))
                closedPlan = user.todo.filter(project__in=self.projects, dateClose__range=(self.dateFrom, self.dateTo))\
                    .values('planTime').annotate(score=Sum('planTime'))
                if closedPlan:
                    closedPlan = closedPlan[0]['score']
                if x['score']:
                    self.rows.append({
                        'cols': [
                            {
                                'url': '/user_detail/?id='+str(x['user']),
                                'text': user.last_name + ' ' + user.first_name
                            },
                            {
                                'text': round(x['score'] / 3600., 2)
                            },
                            {
                                'text': closedPlan or 0
                            }
                        ]
                    })
            except User.DoesNotExist:
                pass

def widget(request, headerValues, a, b):
    filt = {}
    daysBeforeNowForStartFilt = 7
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())

    if 'date_from' in request.POST:
        filt['dateFrom'] = templateTools.dateTime.convertToDateTime(request.POST.get('date_from'))
    else:
        filt['dateFrom'] = now - datetime.timedelta(days=daysBeforeNowForStartFilt)

    if 'date_to' in request.POST:
        filt['dateTo'] = templateTools.dateTime.convertToDateTime(request.POST.get('date_to'))
    else:
        filt['dateTo'] = now

    filt['projects'] = []
    for pid in request.REQUEST.getlist('pid'):
        filt['projects'].append(int(pid))

    if not filt['projects']:
        if headerValues['CURRENT_PROJECT']:
            filt['projects'].append(headerValues['CURRENT_PROJECT'].id)

    projects = PM_Project.objects.filter(closed=False, locked=False)
    if filt['projects']:
        projects = projects.filter(id__in=filt['projects'])

    payChart = PaymentChart(filt['dateFrom'], filt['dateTo'], projects)
    loanChart = sumLoanChart(filt['dateFrom'], filt['dateTo'], projects)
    tChart = timeChart(filt['dateFrom'], filt['dateTo'], projects)
    sChart = simpleChart(filt['dateFrom'], filt['dateTo'], projects)
    charts = [payChart, loanChart, tChart, sChart]


    return {
        'charts': charts,
        'filt': filt
    }