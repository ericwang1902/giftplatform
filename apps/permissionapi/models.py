# _*_ coding:utf-8 _*_

__author__ = 'ericwang'
__date__ = '2018/1/22 8:32'

from django.db import models

class books(models.Model):
    bookname = models.CharField(max_length=100)

    def __str__(self):
        return self.bookname