# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'

from django.http import HttpResponseForbidden, HttpResponse
from PManager.services.access import assets_access
from PManager.widgets.project_statistic.widget import sumLoanChart
from PManager.viewsExt.tools import templateTools
from PManager.models import PM_Project
import headers

import datetime
import xlsxwriter
import StringIO
from django.utils import timezone
from django.core.servers.basehttp import FileWrapper


def protected_file(request):
    if not assets_access(request.user, request.GET.get('uri', None)):
        return HttpResponseForbidden()
    response = HttpResponse()
    response['X-Accel-Redirect'] = request.GET.get('uri', None)
    response['Content-Type'] = ''
    return response

def stat_excel(request):
    print request.GET
    if 'excel' in request.GET:
        filter = {}
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        daysBeforeNowForStartFilt = 7

        headerValues = headers.initGlobals(request)

        if 'date_from' in request.GET:
            filter['dateFrom'] = templateTools.dateTime.convertToDateTime(request.GET.get('date_from'))
        else:
            filter['dateFrom'] = now - datetime.timedelta(days=daysBeforeNowForStartFilt)

        if 'date_to' in request.GET:
            filter['dateTo'] = templateTools.dateTime.convertToDateTime(request.GET.get('date_to'))
        else:
            filter['dateTo'] = now

        filter['projects'] = []
        if headerValues['CURRENT_PROJECT']:
            filter['projects'].append(headerValues['CURRENT_PROJECT'].id)

        projects = PM_Project.objects.filter(closed=False, locked=False)
        if filter['projects']:
            projects = projects.filter(id__in=filter['projects'])

        loanChart = sumLoanChart(filter['dateFrom'], filter['dateTo'], projects)

        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)
        if request.GET.get('excel') == 'loan':
            workbook = loanChart.excel(workbook)
        workbook.close()

        xlsx_data = output.getvalue()

        response = HttpResponse(xlsx_data, mimetype='application/vnd.ms-excel')
        response['Content-Type'] = 'application/vnd.ms-excel'
        # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        # response.write(xlsx_data)
        # response.write(output)

        return response
