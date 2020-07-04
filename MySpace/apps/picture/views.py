from django.core.cache import cache
from django.db.models import Count
from django.views.generic import ListView
from .models import Album, Image
from ..utils.mixin import NavViewMixin


class AlbumView(NavViewMixin, ListView):

    model = Album

    paginate_by = 8

    template_name = 'album.html'

    context_object_name = 'album_list'

    def get_queryset(self):

        cache_key = 'context:%s:list' % self.model._meta.model_name
        album_list = cache.get(cache_key)

        if album_list is None:
            fields = (
                'id', 'name', 'cover', 'desc', 'create_time', 'visit'
            )

            album_list = Album.objects.annotate(img_count=Count('image')). \
                filter(status=Album.STATUS_NORMAL).values(*fields, 'img_count')
            cache.set(cache_key, album_list, 3600)

        return album_list


class ImageView(ListView):

    model = Image

    paginate_by = 12

    template_name = 'picture.html'

    context_object_name = 'picture_list'

    def get_queryset(self):

        cache_key = 'context:%s:list' % self.model._meta.model_name
        picture_list = cache.get(cache_key)

        if picture_list is None:
            fields = (
                'id', 'name', 'cover', 'desc', 'create_time', 'visit'
            )

            picture_list = Album.objects.annotate(img_count=Count('imagemanager')). \
                filter(status=Album.STATUS_NORMAL).values(*fields, 'img_count')
            cache.set(cache_key, picture_list, 3600)

        return picture_list

