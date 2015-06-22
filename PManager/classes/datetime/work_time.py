import datetime
from django.utils import timezone
class WorkTime(object):
    taskHours = 0
    taskRealTime = 0
    startDateTime = None
    endDateTime = None
    startWorkDay = 10
    endWorkDay = 19
    holyDays = [6, 7]

    def __init__(self,*args,**kargs):

        if kargs['taskHours'] and kargs['startDateTime']:
            self.taskHours = kargs['taskHours']
            try:
                self.startDateTime = timezone.make_aware(kargs['startDateTime'], timezone.get_default_timezone())
            except ValueError:
                self.startDateTime = kargs['startDateTime']

            self.taskRealTime = self.cropHolyDays()
            self.endDateTime = self.startDateTime + datetime.timedelta(hours=self.taskRealTime)

    def isHolyday(self,day):
        return day in self.holyDays

    def cropHolyDays(self):
        allTime = 0
        curHour = 0
        curDay = 0
        iterations = 0
        timeLength = self.taskHours
        if not self.holyDays:
            self.holyDays = [6, 7]

        if timeLength > 0:
            while curHour < timeLength and iterations < 1000:
                iterations = iterations + 1

                allTime = self.startDateTime.hour + curHour
                curDay = (self.startDateTime + datetime.timedelta(hours=curHour)).isoweekday()

                if allTime > 24:
                    allTime %= 24

                if self.isHolyday(curDay):
                    hoursToEndOfDay = 24 - allTime
                    timeLength += hoursToEndOfDay
                    curHour += hoursToEndOfDay

                    #and next day
                    timeLength += 1
                    curHour += 1
                    continue

                if (allTime >= self.endWorkDay) or (allTime < self.startWorkDay):
                    timeLength += 1

                curHour += 1

        return curHour