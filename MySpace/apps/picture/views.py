from django.core.cache import cache
from django.db.models import Count, QuerySet
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, ListView
from .models import Album, Image
from ..utils.mixin import NavViewMixin, VisitIncrMixin, rich_render


class AlbumListView(NavViewMixin, ListView):

    model: 'model.Model' = Album

    paginate_by: int = 4

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


class AlbumDetailView(NavViewMixin, VisitIncrMixin, View):

    offset: int = 12
    # template_name: str = 'album_detail.html'
    # context_object_name: str = 'image_list'

    model: 'model.Model' = Album   # visitIncrMixin 依赖它获取 模型类
    pk_url_kwarg: str = 'id'   # visitIncrMixin 依赖它获取 具体的实例

    def get(self, *args, **kwargs) -> HttpResponse:
        """ FIXME:ListView 分页逻辑没有缓存查询结果 多一次 count 查询 ！"""

        ajax_flag = self.request.is_ajax()
        pk: int = self.kwargs.get('id')
        start: int = 0 if self.request.GET.get('start') is None else self.request.GET.get('start')
        offset: int = 10 or int(self.request.GET.get('offset'))
        cache_key: str = f'context:{Image._meta.app_label}:{Image._meta.model_name}:list:by:{self.model._meta.model_name}:{pk}:limit:{start}:{offset}'
        image_list: list = cache.get(cache_key)

        if not image_list:
            fields: tuple = (
                'desc', 'visit', 'thumbnail', 'create_time', 'img',   # Image msg.
                'album__desc', 'album__name'   # Album msg.
            )

            image_qs: QuerySet = Image.objects.filter(album_id=pk).prefetch_related('album').values(*fields)
            start = int(start)
            image_qs: QuerySet = image_qs[start:start + offset]
            # image_qs: QuerySet = Album.objects.filter(id=pk).prefetch_related('image_set').values(*fields)[start:start + offset]
            # TODO：简单粗暴缓解 redis 穿透，实现中间件层逻辑时增加一些优雅的策略
            # 立即执行SQL 以确定是否有结果，QuerySet.exists 方法会产生额外的SQL查询

            image_list: list = [obj for obj in image_qs]
            life: int = 5 if image_list else 60
            cache.set(cache_key, image_list, life * 60)
        if ajax_flag:
            image_list: list = [line for line in image_list]
            return JsonResponse({'status': True, 'image_list': image_list})

        return rich_render(self.request, 'album_detail.html', context={"image_list": image_list})


class ImageView(VisitIncrMixin, View):
    """ 计划是图片的详细信息或者一些其他的什么，似乎暂时用不到～ """

    pk_url_kwarg: str = 'image_id'
    model: 'model.Model' = Image

    def dispatch(self, request, *args, **kwargs) -> 'get:JsonResponse':

        return self.get(*args, **kwargs)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        msg: dict = {'code': 0, 'status': 0, 'data': None}

        return JsonResponse(msg)

