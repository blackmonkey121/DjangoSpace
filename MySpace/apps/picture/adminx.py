#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import xadmin
from xadmin.layout import Row, Fieldset
from .xadminforms import AlbumAdminForm, ImageAdminForm
from django.utils.html import format_html
from django.urls import reverse
from .models import Album, Image


class ImageInline(object):
    form_layout: tuple = (

        Fieldset(
            '照片',
            Row('desc'),
            Row('status', 'visit'),
            Row('img',),
        ),
    )
    extra: int = 2  # 控制额外多几个
    model: 'model.Model' = Image


@xadmin.sites.register(Album)
class AlbumAdmin(object):

    form: 'FormModel' = AlbumAdminForm

    inlines: (list, tuple) = [ImageInline, ]

    list_display: (list, tuple) = ('name', 'desc', 'visit', 'create_time',
                    'status', 'operator', 'image_count')

    list_display_links: (list, tuple) = ['name']  # 在展示的字段上 添加的超链接

    list_filter: (list, tuple) = ['create_time']  # 过滤字段

    search_fields: (list, tuple) = ['name', 'desc']  # 检索的字段

    form_layout: (list, tuple) = (
        Fieldset(
            '相册信息',
            Row('name',),
            Row('desc'),
            Row('cover'),
            Row('status', 'visit'),
        ),
    )

    def operator(self, obj) -> str:
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:picture_album_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def image_count(self, obj, *args, **kwargs) -> int:

        return obj.image_set.count()

    image_count.short_description = '数量'


@xadmin.sites.register(Image)
class ImageAdmin(object):

    form = ImageAdminForm

    list_display: (list, tuple) = ('name', 'album', 'visit', 'status', 'create_time', 'operator', )

    list_display_links: (list, tuple) = ['name']  # 在展示的字段上 添加的超链接

    list_filter: (list, tuple) = ['create_time']  # 过滤字段

    search_fields: (list, tuple) = ['album', 'desc']  # 检索的字段

    form_layout: (list, tuple) = (
        Fieldset(
            '相片信息',
            Row('status', 'visit'),
            Row('img', 'album', ),
            Row('desc'),
        ),
    )

    def operator(self, obj) -> str:
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:picture_image_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def name(self, obj) -> str:
        return '%s id:%s' % (obj.album.name, obj.id)

    name.short_description = '名称'


