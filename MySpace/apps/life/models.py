from django.db import models

# Create your models here.

from ..utils.basemodel import BaseModel, VisitBaseModel


class CookingTag(BaseModel):
    name = models.CharField(max_length=32, blank=False, verbose_name="菜名")

    def __str__(self):
        return self.name


class Cooking(VisitBaseModel):

    name = models.CharField(max_length=32, blank=False, verbose_name="菜名")
    ingredients = models.CharField(max_length=256, blank=False, verbose_name='食材')
    context = models.CharField(max_length=1024, blank=False, verbose_name='步骤/心得')
    tag = models.ForeignKey(to='CookingTag', verbose_name='标签', on_delete=models.DO_NOTHING)
    # file

    def __str__(self):
        return self.name


class Book(VisitBaseModel):
    """ 琐碎的感悟 """

    name = models.CharField(max_length=32, blank=False, verbose_name='书名')
    desc = models.CharField(max_length=512, blank=False, verbose_name='概述')
    cover = models.ImageField(upload_to='cover_book/', width_field=420, height_field=594, verbose_name='封面', default='cover_book/default.png')


class Note(VisitBaseModel):
    """ 随笔 """
    title = models.CharField(max_length=32, blank=False, verbose_name='篇名')
    context = models.CharField(max_length=1024, blank=False, verbose_name='正文')
    book = models.ForeignKey('Book', verbose_name='书籍', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Perception(VisitBaseModel):

    context = models.CharField(max_length=1024, blank=False, verbose_name='感悟')

