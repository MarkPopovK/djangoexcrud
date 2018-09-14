from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.

class TrackPoint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date.strftime('%x %X')

    def timestamp(self):
        return self.date.timestamp()

    def get_points_from_same_user(self):
        points = TrackPoint.objects.all().order_by('date')
        points = points.filter(owner=self.owner)
        return points

    def get_points_from_today(self):
        points = self.get_points_from_same_user()

        # wouldn't work if user and server were in very different time zones tho
        today = timezone.now().date()
        points = points.filter(date__gte=today)
        return points

    def get_total_time(self):
        def get_h_m_s(tdelta):
            total_seconds = int(tdelta.total_seconds())
            hours, remainder = divmod(total_seconds, 60 * 60)
            minutes, seconds = divmod(remainder, 60)
            return hours, minutes, seconds

        def delta_str(hours, minutes, seconds):
            deltaStr = ''
            if hours:
                deltaStr += ' ' + str(hours) + ' hour' + 's'*bool(hours-1)
            if minutes:
                deltaStr += ' ' + str(minutes) + ' minute' + 's'*bool(minutes-1)
            if seconds:
                deltaStr += ' ' + str(seconds) + ' second' + 's'*bool(seconds-1)
            return deltaStr.strip()

        points = self.get_points_from_today()
        elapsed = timedelta(hours=0)
        tracking = False
        segments = []
        for point in points:
            if point.start and not tracking:
                trackStart = point.date
                tracking = True
            elif not point.start and tracking:
                deltaTime = point.date - trackStart
                elapsed += deltaTime
                deltaStr = delta_str(*get_h_m_s(deltaTime))
                segments.append((trackStart.strftime('%X'), point.date.strftime('%X'), deltaStr))
                tracking = False
        if tracking:
            deltaTime = timezone.now() - trackStart
            elapsed += deltaTime
            segments.append((trackStart.strftime('%X'), 'Active', delta_str(*get_h_m_s(deltaTime))))
        rested = (timezone.now() - points.first().date) - elapsed
        rested = get_h_m_s(rested)
        rested = delta_str(*rested)

        elapsedSeconds = elapsed.total_seconds()
        elapsed = get_h_m_s(elapsed)
        elapsed = delta_str(*elapsed)
        return elapsed, rested, segments, elapsedSeconds
