from django.db import models
from django.db.models import Manager
from django.utils.safestring import mark_safe
import mistune
from mdeditor.fields import MDTextField
from ..utils.basemodel import VisitBaseModel, BaseModel
from xadmin.views.edit import *

class ArticleManager(Manager):

    def get_abstract_all(self):
        return super(ArticleManager, self).all()

    def filter(self, *args, **kwargs):
        return super(ArticleManager, self).filter(status=self.model.STATUS_NORMAL, *args, **kwargs)

    def all(self):
        return super(ArticleManager, self).filter(status=self.model.STATUS_NORMAL)


class Category(BaseModel):

    name = models.CharField(max_length=50, verbose_name="名称")

    def get_cache_keys(self) -> set:
        ret_set: set = {
            f'context:article:article:list:by:{self._meta.model_name}:{self.id}',
            f'context:{self._meta.app_label}:{self._meta.model_name}:list'
        }
        return ret_set

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"
        # ordering = ['-id', ]


class Tag(BaseModel):

    name = models.CharField(max_length=10, verbose_name="名称")

    def get_cache_keys(self) -> set:
        ret_set: set = {
            f'context:{self._meta.app_label}:article:list:by:{self._meta.model_name}:{self.id}',
            f'context:{self._meta.app_label}:{self._meta.model_name}:list'
        }
        return ret_set

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
    init_objects = Manager()
    objects = ArticleManager()

    # @classmethod
    # def get_hot_articles(cls):
    #
    #     return cls.objects.filter(status=cls.STATUS_NORMAL).select_related('category')
    #
    # @classmethod
    # def get_latest_article(cls):
    #
    #     return cls.objects.filter(status=cls.STATUS_NORMAL).select_related('category')

    def get_cache_keys(self) -> set:

        related_cache_key: set = {
            f'context:{self._meta.app_label}:{self._meta.model_name}:list',  # 文章列表缓存
            f'context:{self._meta.app_label}:{self._meta.model_name}:list:by:category:{self.category_id}',  # 关联的分类
        }

        try:
            related_cache_key.add(
                f'context:{self._meta.app_label}:{self._meta.model_name}:{self.id}:detail'
            )
        except Exception as e:
            print(e)
        print(related_cache_key)
        # FIXME: 对于新增对象，无法获取多对多字段的缓存 键 ～ 无法及时刷新cache.
        return related_cache_key ^ {f'context:{self._meta.app_label}:{self._meta.model_name}:list:by:tag:{tag.get("id")}' for tag in self.tag.values('id')}

    def save(self, *args, **kwargs) -> None:
        """ 重写文章主体 """
        safe_content = mark_safe(self.content)
        self.content_html = mistune.markdown(safe_content)
        super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id', ]   # 按照id降序排列

    def __str__(self):
        return self.title