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
    form_layout = (

        Fieldset(
            '照片',
            Row('desc'),
            Row('status', 'visit'),
            Row('img',),
        ),
    )
    extra = 2  # 控制额外多几个
    model = Image


@xadmin.sites.register(Album)
class AlbumAdmin(object):

    form = AlbumAdminForm

    inlines =[ImageInline, ]

    list_display = ('name', 'desc', 'visit', 'create_time',
                    'status', 'operator', 'image_count')

    list_display_links = ['name']  # 在展示的字段上 添加的超链接

    list_filter = ['create_time']  # 过滤字段

    search_fields = ['name', 'desc']  # 检索的字段

    form_layout = (
        Fieldset(
            '相册信息',
            Row('name',),
            Row('desc'),
            Row('cover'),
            Row('status', 'visit'),
        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:picture_album_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def image_count(self, obj, *args, **kwargs):
        """

        :return:

        """
        return obj.imagemanager_set.count()

    image_count.short_description = '数量'


@xadmin.sites.register(Image)
class ImageAdmin(object):

    form = ImageAdminForm

    list_display = ('desc', 'visit', 'status', 'album', 'create_time', 'operator', )

    list_display_links = ['name']  # 在展示的字段上 添加的超链接

    list_filter = ['create_time']  # 过滤字段

    search_fields = ['album', 'desc']  # 检索的字段

    form_layout = (
        Fieldset(
            '相片信息',
            Row('status', 'visit'),
            Row('img', 'album', ),
            Row('desc'),
        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:picture_image_change', args=(obj.id,))
        )

    operator.short_description = '操作'

