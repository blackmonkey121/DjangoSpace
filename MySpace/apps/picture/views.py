from django.core.cache import cache
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from django.views.generic import View, ListView
from .models import Album, Image
from ..utils.mixin import NavViewMixin, VisitIncrMixin


class AlbumListView(NavViewMixin, ListView):

    model: 'model.Model' = Album

    paginate_by: int = 8

    template_name: str = 'album.html'

    context_object_name: str = 'album_list'

    def get_queryset(self) -> QuerySet:

        cache_key: str = f'context:{self.model._meta.app_label}:{self.model._meta.model_name}:list'
        album_qs: QuerySet = cache.get(cache_key)

        if album_qs is None:
            fields: tuple = (
                'id', 'name', 'cover', 'desc', 'create_time', 'visit'
            )

            album_qs: QuerySet = Album.objects.annotate(img_count=Count('image')). \
                filter(status=Album.STATUS_NORMAL).values(*fields, 'img_count')
            cache.set(cache_key, album_qs, 3600)

        return album_qs


class AlbumDetailView(NavViewMixin, VisitIncrMixin, ListView):

    paginate_by: int = 8
    template_name: str = 'album_detail.html'
    context_object_name: str = 'image_list'

    model: 'model.Model' = Album   # visitIncrMixin 依赖它获取 模型类
    pk_url_kwarg: str = 'id'   # visitIncrMixin 依赖它获取 具体的实例

    def get_queryset(self) -> QuerySet:
        """ FIXME:ListView 分页逻辑没有缓存查询结果 多一次 count 查询 ！"""

        pk: int = self.kwargs.get('id')
        cache_key: str = f'context:{Image._meta.app_label}:{Image._meta.model_name}:list:by:{self.model._meta.model_name}:{pk}'
        image_qs: QuerySet = cache.get(cache_key)

        if not image_qs:
            fields: tuple = (
                'image__desc', 'image__visit', 'image__img', 'image__create_time',   # Image msg.
                'desc', 'name'   # Album msg.
            )
            image_qs: QuerySet = Album.objects.filter(id=pk).prefetch_related('image_set').values(*fields)
            # TODO：简单粗暴缓解 redis 穿透，实现中间件层逻辑时增加一些优雅的策略
            life: int = 5 if image_qs.exists() else 60
            cache.set(cache_key, image_qs, life * 60)

        return image_qs


class ImageView(VisitIncrMixin, View):
    """ 计划是图片的详细信息或者一些其他的什么，似乎暂时用不到～ """

    pk_url_kwarg: str = 'image_id'
    model: 'model.Model' = Image

    def dispatch(self, request, *args, **kwargs) -> 'get:JsonResponse':

        return self.get(*args, **kwargs)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        msg: dict = {'code': 0, 'status': 0, 'data': None}

        return JsonResponse(msg)

