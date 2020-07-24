import datetime

from django.db.models import QuerySet
from django.views.generic.base import View
from django.views.generic.list import ListView

from .models import Article
from ..comment.models import ArticleComment
from ..utils.mixin import NavViewMixin, VisitIncrMixin, rich_render
from ..utils.tools import proxy_query


class ArticleView(NavViewMixin, ListView):
    """ 抽象类 """
    paginate_by = 10

    allow_empty = True

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
        query_filter: dict = kwargs.get('query_filter')
        # 看是否有自定义的查询字段
        fields: tuple = kwargs.get('fields')

        order_by = kwargs.get('order') or '-id'

        if isinstance(query_filter, dict):
            qs = qs.filter(**query_filter)

        fields: tuple = fields or self.fields

        # 一次SQL查询完所有值, 防止在模版中遍历 执行n次 SQL查询
        return qs.values(*fields).order_by(order_by)


class ArticleListView(ArticleView):
    """ 文章列表试图 """

    def get_queryset(self, *args, **kwargs) -> QuerySet:

        # 缓存键
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list'
        func = super(ArticleListView, self).get_queryset
        return proxy_query(key=cache_key, func=func, timeout=3600)


class CategoryListView(ArticleView):
    """ Category of articles by tag. """

    def get_queryset(self) -> QuerySet:

        category_id: int = self.kwargs.get('id')
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list:by:category:{category_id}'
        query_filter: dict = {'category': category_id}
        func = super(CategoryListView, self).get_queryset

        return proxy_query(key=cache_key, func=func, query_filter=query_filter)


class TagListView(ArticleView):
    """ 这与 category 的list 视图 几乎一摸一样，但是还是不抽取公共代码的好～  """

    def get_queryset(self) -> QuerySet:

        tag_id: int = self.kwargs.get('id')
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list:by:tag:{tag_id}'
        query_filter: dict = {'tag': tag_id}
        func = super(TagListView, self).get_queryset

        return proxy_query(key=cache_key, func=func, query_filter=query_filter)


class ArchiveListView(ArticleView):
    """  List of articles by create time. """

    def get_queryset(self) -> QuerySet:

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
        # 拼接cache键
        cache_key: str = f'{start}-{end}'
        func = super(ArchiveListView, self).get_queryset
        query_filter: dict = {'create_time__range': (start, end)}  # 过滤条件

        return proxy_query(key=cache_key, func=func, query_filter=query_filter)


class ArticleDetailView(VisitIncrMixin, View):
    """ 文章详情视图 """
    template_name = 'article_detail.html'
    model = Article

    def get(self, request, *args, **kwargs) -> 'HttpResponse':

        article_id = self._pk = kwargs.get('id')
        # 获取文章详情和标签信息
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:detail:{article_id}'
        context: dict = proxy_query(key=cache_key, func=self.query_article, article_id=article_id)

        # 获取文章评论（因为评论信息改动较为频繁，且需要尽可能快的更新，so 单独缓存）
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:comment:{article_id}'
        comment_qs: list = proxy_query(key=cache_key, func=self.query_comment, article_id=article_id)

        # 最热文章
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:hot'
        article_hot: QuerySet = proxy_query(key=cache_key, func=self.model.query_hot_article, count=10)

        # 最新文章
        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:new'
        article_new: QuerySet = proxy_query(key=cache_key, func=self.model.query_new_article, count=10)

        # 相关推荐

        # 拼接上下文
        context.update({'comment_list': comment_qs})   # 评论列表
        context.update({'article_hot': article_hot})   # 最热文章
        context.update({'article_new': article_new})   # 最新文章


        # 添加浏览
        response = rich_render(request, 'article_detail.html', context=context, *args, **kwargs)
        self.handle_visited(request, *args, **kwargs)   # 增加访问
        return response

    def query_article(self, article_id, *args, **kwargs) -> dict:
        """
        查询文章详情
        @param article_id:  文章ID
        @return: QuerySet 文章详情 带文章标签
        """
        fields: tuple = (
            'id', 'title', 'content_html', 'create_time', 'visit', 'content_html',
            'category__id', 'category__name', 'tag__id', 'tag__name',
        )

        if hasattr(self, '_pk'):
            article_id: int = getattr(self, '_pk')

        query: QuerySet = Article.objects.filter(id=article_id).prefetch_related('tag').select_related('category').values(*fields)
        article: dict = dict()
        tag_list: list = list()
        for record in query.iterator():
            if not article:
                article = record
            tag_list.append({'id': record.get('tag__id'), 'name': record.get('tag__name')})

        return {'article': article, 'tags': tag_list}

    def query_comment(self, article_id, *args, **kwargs) -> QuerySet:
        """
        查询评论
        @param article_id: 文章ID  type:int
        @return: 可见评论查询集  type: QuerySet
        """
        fields: tuple = ('id', 'create_time', 'context')
        if hasattr(self, '_pk'):
            article_id: int = getattr(self, '_pk')

        query: QuerySet = ArticleComment.objects.filter(article_id=article_id).values(*fields)
        return query

    # @staticmethod
    # def query_hot_article() -> QuerySet:
    #     """
    #     最热文章
    #     @return:
    #     """
    #     fields: tuple = ('id', 'title', 'visit')
    #     query: QuerySet = Article.objects.values(*fields).order_by('-visit')[:10]
    #     return query
    #
    # @staticmethod
    # def query_new_article() -> QuerySet:
    #     """
    #     最新文章
    #     @return:
    #     """
    #     fields: tuple = ('id', 'title')
    #     query: QuerySet = Article.objects.values(*fields).order_by('-id')[:10]
    #     return query

    # @staticmethod
    # def query_top_article() -> QuerySet:
    #     """
    #     置顶
    #     @return:
    #     """
    #
    # def query_recommend_article(self) -> QuerySet:
    #     """
    #     相似度推荐
    #     @return:
    #     """