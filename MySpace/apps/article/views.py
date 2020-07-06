from abc import ABCMeta

from django.core.cache import cache
from django.db.models import F

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Article
from ..utils.mixin import NavViewMixin, VisitIncrMixin
import datetime


class ArticleView(NavViewMixin, ListView, metaclass=ABCMeta):
    """ 抽象类 """
    paginate_by = 10

    context_object_name = "article_list"

    template_name = "article_list.html"

    model = Article


class ArticleListView(ArticleView):
    """ 文章列表试图 """

    def get(self, request, *args, **kwargs):

        return super(ArticleListView, self).get(request, *args, **kwargs)


class CategoryListView(ArticleView):
    """ Category of articles by tag. """

    def get_queryset(self):
        id = self.kwargs.get('id')
        qs = Article.objects.filter(category_id=id).select_related('category')

        return qs


class TagListView(ArticleView):
    """ List of articles by tag. """

    def get_queryset(self):
        id = self.kwargs.get('id')
        qs = Article.objects.filter(tag=id).select_related('category')

        return qs


class ArchiveListView(ArticleView):
    """  List of articles by create time. """

    def get_queryset(self):

        year = self.kwargs.get('year', 2019)
        month = self.kwargs.get('month', 0)

        if 0 < month < 13:
            days = (datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)).days
            start = datetime.date(year, month, 1)
            end = datetime.date(year, month, days)
        else:
            start = datetime.date(year, 1, 1)
            end = datetime.date(year, 12, 31)

        qs = Article.objects.filter(create_time__range=(start, end))

        return qs


class ArticleDetailView(NavViewMixin, VisitIncrMixin, DetailView):
    """  """
    pk_url_kwarg = 'id'
    model = Article
    template_name = 'article_detail.html'

    def get_queryset(self):

        return Article.objects.all().select_related('category')
