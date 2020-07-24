from django.db.models import QuerySet
from django.views.generic import View
from ..utils.mixin import rich_render, CacheMixin
from ..utils.tools import proxy_query
from ..article.models import Article
from ..picture.models import Album

# Create your views here.


# 首页缓整个页面
class HomeView(CacheMixin, View):

    cache_timeout: int = 5 * 60  # 首页缓存时间
    article_count: int = 6   # 首页展示文章个数
    album_count: int = 8   # 首页展示相册个数

    def get(self, request, *args, **kwargs):

        context: dict = dict()  # 初始化页面上下文
        context.update(self.query_article())   # 更新文章页上下文数据
        context.update(self.query_album())   # 更新相册上下文数据
        # context.update(self.query_life())    # 更新 生活上下文数据
        # context.update(self.query_travel())    # 更新足迹上下文数据

        return rich_render(request, 'home.html', context=context)

    def query_article(self) -> dict:
        """ 获取最新最热文章 """
        article_count = 10
        if hasattr(self, 'article_count'):
            article_count = self.article_count

        cache_key: str = f'context:{Article._meta.app_label}:{Article._meta.model_name}:hot'
        article_hot: QuerySet = proxy_query(key=cache_key, func=Article.query_hot_article, count=10)[:article_count]

        cache_key: str = f'context:{Article._meta.app_label}:{Article._meta.model_name}:new'
        article_new: QuerySet = proxy_query(key=cache_key, func=Article.query_new_article, count=10)[:article_count]

        context: dict = {
            'article_hot': article_hot,
            'article_new': article_new,
            # 'tags_list': tag_list,     rich_render 会填充 tag_list 字段到上下文
        }

        return context

    def query_album(self) -> dict:
        """ 获取相册 """
        cache_key: str = f'context:home:album:list'

        album_count: int = 8
        if hasattr(self, 'album_count'):
            album_count = self.album_count

        def inner_query(count, *args, **kwargs) -> QuerySet:
            fields: tuple = ('id', 'cover',)
            return Album.objects.values(*fields)[:count]

        album_list: QuerySet = proxy_query(key=cache_key, func=inner_query, count=album_count)

        return {'album_list': album_list}

    def query_life(self) -> dict:
        """  """

    def query_travel(self) -> dict:
        """ 旅程列表 """


class AboutMe(View):

    def get(self, request, *args, **kwargs):
        return rich_render(request, 'me.html')


class AllSiteSearch(View):
    """
    分apps 展示内容 提供连接
    """
