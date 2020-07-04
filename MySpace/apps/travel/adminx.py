#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import xadmin
from xadmin.layout import Row, Fieldset
from .xadminforms import TravelAdminForm
from django.utils.html import format_html
from django.urls import reverse
from .models import Travel, Province, City, Point, ImageManager


class PointInline(object):
    form_layout = (

        Fieldset(
            '基础信息',
            Row('title', 'status'),
            Row('addr', 'city'),

        ),
        Fieldset(
            '景点描述',
            Row('context',)
        )
    )
    extra = 1  # 控制额外多几个
    model = Point


class ImageInline(object):
    form_layout = (

        Fieldset(
            '照片',
            Row('desc'),
            Row('status', 'visit'),
            Row('img',),
        ),
    )
    extra = 4  # 控制额外多几个
    model = ImageManager


class CityInline(object):
    form_layout = (

        Fieldset(
            '城市',
            Row('name', 'status'),
            Row('desc'),
            Row('cover'),
        ),
    )
    extra = 1  # 控制额外多几个
    model = City


@xadmin.sites.register(Travel)
class TravelAdmin(object):
    # 后端管理页面的渲染会按照模型表定义的来生成HTML元素 这是给予ModelAdmin和ModelForm的
    # 写一个我们自己的form，指定给ModelAdmin就OK了
    # form字段  PostAdminForm 在 adminforms.py 中

    form = TravelAdminForm

    inlines = (PointInline,)

    list_display = ('title', 'context', 'visit',
                    'status', 'operator', 'province')

    list_display_links = ['title']  # 在展示的字段上 添加的超链接

    list_filter = ['create_time']  # 过滤字段

    search_fields = ['title', 'context', 'province']  # 检索的字段

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'province'),
            Row('status', 'visit',),

        ),
        Fieldset(
            '旅程描述',
            'context',
        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:travel_travel_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@xadmin.sites.register(Point)
class PointAdmin(object):

    inlines =[ImageInline, ]

    list_display = ('title', 'addr',
                    'status', 'operator', 'city')

    list_display_links = ['title']  # 在展示的字段上 添加的超链接

    list_filter = ['create_time']  # 过滤字段

    search_fields = ['title', 'context', 'city']  # 检索的字段

    form_layout = (
        Fieldset(
            '基础信息',

            Row('travel'),
            Row('title', 'status'),
            Row('addr', 'city'),

        ),
        Fieldset(
            '详细信息',
            Row('context',)
        )
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:travel_point_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@xadmin.sites.register(Province)
class ProvinceAdmin(object):

    inlines = [CityInline,]

    list_display = ('name', 'status', 'operator', 'desc', 'cover' )

    list_display_links = ['name',]  # 在展示的字段上 添加的超链接

    list_filter = ['create_time', 'name']  # 过滤字段

    search_fields = ['name',]  # 检索的字段

    form_layout = (
        Fieldset(
            '省份',
            Row('name', 'status'),
            Row('desc'),
            Row('cover'),
        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:travel_province_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@xadmin.sites.register(City)
class CityAdmin(object):

    list_display = ('name',
                    'status', 'desc', 'cover')

    list_display_links = ['name',]  # 在展示的字段上 添加的超链接

    list_filter = ['create_time', 'name']  # 过滤字段

    search_fields = ['name',]  # 检索的字段

    form_layout = (
        Fieldset(
            '城市',
            Row('name', 'status', ),
            Row('cover', 'province',),
            Row('desc'),

        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:travel_province_change', args=(obj.id,))
        )

    operator.short_description = '操作'
