from django.db import models
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

import mistune
from mdeditor.fields import MDTextField
from ..utils.basemodel import VisitBaseModel, BaseModel


class Category(BaseModel):

    name = models.CharField(max_length=50, verbose_name="名称")

    def flush_cache_keys(self) -> dict:

        self.CACHE_DICT['keys'] = {
            f'context:{self._meta.app_label}:article:list:by:{self._meta.model_name}:{self.id}',  # 按分类划分的文章列表
            f'context:{self._meta.app_label}:{self._meta.model_name}:list'   # 分类列表
        }
        return self.CACHE_DICT

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"
        # ordering = ['-id', ]


class Tag(BaseModel):

    name = models.CharField(max_length=10, verbose_name="名称")

    def flush_cache_keys(self) -> dict:
        self.CACHE_DICT['keys'] = {
            f'context:{self._meta.app_label}:article:list:by:{self._meta.model_name}:{self.id}',   # 按标签划分的文章列表
            f'context:{self._meta.app_label}:{self._meta.model_name}:list'   # 标签列表
        }
        return self.CACHE_DICT

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

    def flush_cache_keys(self) -> dict:

        self.CACHE_DICT['keys'] = {
            f'context:{self._meta.app_label}:{self._meta.model_name}:list',  # 文章列表缓存
            f'context:{self._meta.app_label}:{self._meta.model_name}:list:by:category:{self.category_id}',  # 关联的分类
            f'context:{self._meta.app_label}:{self._meta.model_name}:detail:{self.id}',  # 文章详情
            f'context:{self._meta.app_label}:{self._meta.model_name}:new',   # 最新文章
            f'context:{self._meta.app_label}:{self._meta.model_name}:hot',   # 最热文章
        }

        self.CACHE_DICT['match'] = {f'context:{self._meta.app_label}:{self._meta.model_name}:list:by:tag:*'}   # 所有按标签分类文章列表

        return self.CACHE_DICT

    def save(self, *args, **kwargs) -> None:
        """ 重写文章主体 """
        safe_content = mark_safe(self.content)
        self.content_html = mistune.markdown(safe_content)
        super(Article, self).save(*args, **kwargs)

    @classmethod
    def query_hot_article(cls, count: int = 6, *args, **kwargs) -> QuerySet:
        """
        最热文章
        @return:
        """
        fields: tuple = ('id', 'title', 'visit')
        query: QuerySet = cls.objects.values(*fields).order_by('-visit')[:count]
        return query

    @classmethod
    def query_new_article(cls, count: int = 6, *args, **kwargs) -> QuerySet:
        """
        最新文章
        @return:
        """
        fields: tuple = ('id', 'title')
        query: QuerySet = cls.objects.values(*fields).order_by('-id')[:count]
        return query

    @classmethod
    def query_recommend_article(cls, count: int = 6, *args, **kwargs) -> QuerySet:
        """
        相似度推荐
        @return:
        """

    class Meta:
        verbose_name = verbose_name_plural = "文章"

    def __str__(self):
        return self.title