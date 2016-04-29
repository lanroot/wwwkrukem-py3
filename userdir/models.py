# -*- coding: utf8 -*-
import datetime
from django.db import models

# Create your models here.
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, help_text='City Name')
    ccode = models.CharField(max_length=32, help_text='City Phone Prefix')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'cities'
        ordering = ['id']

class Div(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=32)
    mcode = models.CharField(max_length=8, help_text='Meridian Prefix')
    name = models.CharField(max_length=255, help_text='Division Name')
    domain = models.CharField(max_length=128, help_text='E-mail Domain')
#    city_id = models.IntegerField()
    city = models.ForeignKey(City)
    pri = models.SmallIntegerField(help_text='Priority Code')
    addr_pref = models.CharField(max_length=9, help_text='IP Address Prefix')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'divs'
        ordering = ['-pri']

class Person(models.Model):
    pers_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, help_text='Full Name (last, first, middle)')
    gtel = models.CharField(max_length=32, blank=True, help_text='City Phone Number')
    mtel = models.CharField(max_length=32, blank=True, verbose_name='meridian', help_text='Meridian Phone Number')
    stel = models.CharField(max_length=32, blank=True, help_text='Mobile Phone Number')
    fax = models.CharField(max_length=32, blank=True, help_text='Fax Phone Number')
    email = models.EmailField(verbose_name='e-mail')
    post = models.CharField(max_length=255, blank=True, help_text='Job Title')
    office = models.CharField(max_length=255, blank=True, help_text='Room Number')
    subdiv = models.CharField(max_length=255, blank=True)
    visible = models.SmallIntegerField(default=1)
    active = models.SmallIntegerField(default=1)
#    div_id = models.IntegerField()
    div = models.ForeignKey(Div)
    last_update = models.DateTimeField(auto_now_add=True)
#    pri = models.ForeignKey(Div)

    def do_wrong_layout(self):
         _eng_chars = u"~!@$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
         _rus_chars = u"ё!\";%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
         _do_wrong_table = dict(zip(_rus_chars, _eng_chars))
         return u''.join([_do_wrong_table.get(c, c) for c in self.name])

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/userdir/get/%i" % self.pers_id

    class Meta:
        db_table = u'persons'
        ordering = ['div', 'name']

