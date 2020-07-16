from django.core.cache import cache
from django.db.models import QuerySet
from django.views.generic.base import View

from django.views.generic.list import ListView

from .models import Article
from ..utils.mixin import NavViewMixin, VisitIncrMixin, rich_render
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
        qs: QuerySet = self.model.objects.filter()

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
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list'
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

        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list:by:category:{category_id}'
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
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list:by:tag:{tag_id}'
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


class ArticleDetailView(VisitIncrMixin, View):
    """ 文章详情视图 """
    template_name = 'article_detail.html'
    model = Article

    def get(self, request, *args, **kwargs) -> 'TemplateResponse':
        article_id = self._pk = kwargs.get('id')

        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:detail:{article_id}'
        context: dict = cache.get(cache_key)

        if not context:  # 缓存未命中
            from django.db import connection
            # FIXME: 优化SQL索引, 使用存储过程
            SQL: str = """
                select aa.id, aa.title, aa.create_time, aa.visit, aa.content_html, ac.name,at.name, ca.id, ca.context, ca.create_time
                from article_article as aa
                left join article_article_tag as aat on aa.id = aat.article_id
                left join article_category ac on aa.category_id = ac.id
                left join comment_articlecomment ca on aa.id = ca.article_id
                left join article_tag as at on aat.tag_id = at.id
                where aa.id = '%s'"""

            with connection.cursor() as cursor:
                cursor.execute(SQL, article_id)
                ret: tuple = cursor.fetchall()

            if ret:                     # 如果查询集不为空
                article = dict()
                tag: set = set()
                comment: dict = dict()

                article['id'] = ret[0][0]
                article['title'] = ret[0][1]
                article['create_time'] = ret[0][2]
                article['visit'] = ret[0][3]
                article['content_html'] = ret[0][4]
                article['category'] = ret[0][5]

                # 遍历sql得到的数据表转化为模版友好的数据结构
                for line in ret:
                    tag.add(line[6])
                    comment.update({line[7]: (line[8], line[9])})

                context: dict = {
                    'article': article,
                    'tag': tag,
                }

                if list(comment)[0] is not None:   # 如果没有评论数据，就不传给模版上下文
                    context.update(
                        {'comment': comment}
                    )

                life: int = 60
            else:
                life: int = 5  # 缓存未命中，SQL查询为空 ---> 不合法URL 创建临时缓存

            cache.set(cache_key, context, life * 60)

        response = rich_render(request, 'article_detail.html', context=context, *args, **kwargs)
        self.handle_visited(request, *args, **kwargs)   # 增加访问
        return response
