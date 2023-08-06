import datetime

from django.db import models


class VisitCounts(models.Model):
    date = models.DateField(auto_now=True, verbose_name='日期')
    amount_of_day = models.IntegerField(default=0, verbose_name='单日访问量', editable=False)

    def __str__(self):
        return '{0} {1}次'.format(self.date, self.amount_of_day)

    @classmethod
    def today_add_one(cls):
        try:
            counts_today = cls.objects.get(date=datetime.datetime.today())
            counts_today.amount_of_day += 1
        except:
            counts_today = VisitCounts()
            counts_today.amount_of_day += 1
        finally:
            counts_today.save()

    @classmethod
    def get_total_counts(cls):
        sum([i.amount_of_day for i in cls.objects.all()])

    class Meta:
        db_table = "ide_visitor_counts"
        verbose_name = "访问统计"
        verbose_name_plural = "访问统计"


class Visitors(models.Model):
    ip = models.CharField(max_length=15, verbose_name='IP地址', default='unknown', blank=True, editable=False)
    time = models.DateTimeField(auto_now=True, verbose_name='访问时间', editable=False)
    url = models.SlugField(verbose_name='URL', editable=False)

    def __str__(self):
        return 'IP:{0} TIME:{1} URL:{2}'.format(self.ip, self.time, self.url)

    class Meta:
        db_table = "ide_visitor"
        verbose_name = "访问者"
        verbose_name_plural = "访问者"


class MpyMachineIP(models.Model):
    ip = models.CharField(max_length=15, verbose_name='IP地址', default='unknown', blank=True, editable=False)
    machine_ip = models.TextField(verbose_name='Mpy Machine 内网IP地址', default='', editable=False)

    def set_esp_ip(self, esp_ip):
        if esp_ip.replace(',', '') in self.esp_ip.split(','):
            pass
        else:
            self.esp_ip += esp_ip

    def get_esp_ip(self):
        return self.esp_ip.split(',')

    def __str__(self):
        return self.ip

    class Meta:
        db_table = "ide_machine_ip"
        verbose_name = "Mpy Machine IP"
        verbose_name_plural = "Mpy Machine IP"
