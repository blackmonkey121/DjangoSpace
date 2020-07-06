from django.db import models
from django.utils.safestring import mark_safe

import mistune
from mdeditor.fields import MDTextField

from ..utils.basemodel import VisitBaseModel, BaseModel


class Category(BaseModel):

    cache_list: list = [
        'context:category:list',
    ]

    name = models.CharField(max_length=50, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"
        # ordering = ['-id', ]


class Tag(BaseModel):

    name = models.CharField(max_length=10, verbose_name="名称")

    cache_list: list = [
        'context:tag:list',
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        ordering = ['-id', ]


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