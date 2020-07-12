from django.core.cache import cache
from django.db.models import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Article
from ..utils.mixin import NavViewMixin, VisitIncrMixin
import datetime


class ArticleView(NavViewMixin, ListView):
    """ 抽象类 """
    paginate_by = 10

    context_object_name: str = "article_list"

    template_name: str = "article_list.html"

    model: 'model.Model' = Article

    fields: tuple = (
        'id', 'title', 'desc', 'create_time', 'visit', 'category__name'
    )

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """ 获取 status = status.NORMAL 的文章查询集 """

        # 过滤 status=STATUS_NORMAL的文章
        qs: QuerySet = self.model.objects.filter(status=self.model.STATUS_NORMAL)

        # 看是否有其他过滤条件，过滤查询集合
        _filter: dict = kwargs.get('filter')
        # 看是否有自定义的查询字段
        _fields: tuple = kwargs.get('fields')

        if isinstance(_filter, dict):
            qs = qs.filter(**_filter)

        fields: tuple = _fields or self.fields

        # 一次SQL查询完所有值, 防止在模版中遍历 执行n次 SQL查询
        return qs.values(*fields)


class ArticleListView(ArticleView):
    """ 文章列表试图 """

    def get(self, request, *args, **kwargs):

        return super(ArticleListView, self).get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet:

        cache_key: str = f'context:{self.model._meta.model_name}:list'
        qs: QuerySet = cache.get(cache_key)

        if not qs:
            qs: QuerySet = super(ArticleListView, self).get_queryset(*args, **kwargs)
            cache.set(cache_key, qs, 3600)
        return qs


class CategoryListView(ArticleView):
    """ Category of articles by tag. """

    def get_queryset(self) -> QuerySet:

        category_id: int = self.kwargs.get('id')
        if not category_id:
            raise KeyError('Category id is must be required！')

        cache_key: str = f'context:{self.model._meta.model_name}:category:{category_id}:list'
        qs: QuerySet = cache.get(cache_key)

        if not qs:
            _filter: dict = {'category': category_id}
            qs: QuerySet = super(CategoryListView, self).get_queryset(filter=_filter)
            life: int = 5 if qs.exists() else 60  # 防 redis 穿透 即使是错的 id 也要缓存一个值 拦截恶意攻击
            cache.set(cache_key, qs, life * 60)
        return qs


class TagListView(ArticleView):
    """ 这与 category 的list 视图 几乎一摸一样，但是还是不抽取公共代码的好～  """

    def get_queryset(self) -> QuerySet:

        tag_id: int = self.kwargs.get('id')
        if not tag_id:
            raise KeyError('Tag id is must be required！')

        # 查缓存
        cache_key: str = f'context:{self.model._meta.model_name}:category:{tag_id}:list'
        qs: QuerySet = cache.get(cache_key)

        if not qs:
            # 缓存 miss 执行SQL
            _filter: dict = {'tag': tag_id}
            qs: QuerySet = super(TagListView, self).get_queryset(filter=_filter)
            # 按查询照结果 更新缓存
            life: int = 5 if qs.exists() else 60
            cache.set(cache_key, qs, life * 60)

        return qs


class ArchiveListView(ArticleView):
    """  List of articles by create time. """

    def get_queryset(self):

        year: int = self.kwargs.get('year', 2019)
        month: int = self.kwargs.get('month', 0)

        # 获取归档日期区间
        if 0 < month < 13:
            days: int = (datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)).days
            start: datetime.date = datetime.date(year, month, 1)
            end: datetime.date = datetime.date(year, month, days)
        else:
            start: datetime.date = datetime.date(year, 1, 1)
            end: datetime.date = datetime.date(year, 12, 31)
        cache_key: str = f'{start}-{end}'
        qs: QuerySet = cache.get(cache_key)

        _filter: dict = {'create_time__range': (start, end)}

        if not qs:
            qs: QuerySet = super(ArchiveListView, self).get_queryset(filter=_filter)
            life: int = 5 if qs.exists() else 60
            cache.set(cache_key, qs, life * 60)
        return qs


class ArticleDetailView(NavViewMixin, VisitIncrMixin, DetailView):
    """  """
    pk_url_kwarg = 'id'
    model = Article
    template_name = 'article_detail.html'

    def get_queryset(self):

        return Article.objects.all().select_related('category')
