from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.core.cache import cache

import mistune
from mdeditor.fields import MDTextField

from ..utils.basemodel import VisitBaseModel, BaseModel



class Category(BaseModel):

    name = models.CharField(max_length=50, verbose_name="名称")

    class Meta:
        verbose_name = verbose_name_plural = "分类"
        ordering = ['-id', ]

    def __str__(self):
        return self.name


class Tag(BaseModel):

    name = models.CharField(max_length=10, verbose_name="名称")

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        ordering = ['-id', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ 更新缓存 """
        cache_key = 'context:%s:list' % self.__class__.__name__.lower()
        cache.delete(cache_key)
        super().save(*args, **kwargs)


class Article(VisitBaseModel):

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=512, verbose_name='摘要')
    content = MDTextField(verbose_name="正文", help_text="MarkDown格式")
    content_html = models.TextField(verbose_name="正文html", blank=True, editable=False)
    category = models.ForeignKey(Category, verbose_name="文章分类", on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    @classmethod
    def get_hot_articles(cls):

        return cls.objects.filter(status=cls.STATUS_NORMAL).select_related('category')

    @classmethod
    def get_latest_article(cls):

        return cls.objects.filter(status=cls.STATUS_NORMAL).select_related('category')

    def save(self, *args, **kwargs):
        """ 重写文章主体 """
        safe_content = mark_safe(self.content)
        self.content_html = mistune.markdown(safe_content)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id', ]   # 按照id降序排列

    def __str__(self):
        return self.title