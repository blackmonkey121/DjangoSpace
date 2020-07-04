#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import xadmin
from xadmin.layout import Row, Fieldset

from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Article, Tag

from .xadminforms import ArticleAdminForm


xadmin.AdminSite.site_header = 'MySpace '.format(xadmin.AdminSite.urls)
xadmin.AdminSite.site_title = 'MySpace:ClarkMonkey'
xadmin.AdminSite.index_title = 'Manager Page'


@xadmin.sites.register(Category)
class CategoryAdmin(object):
    # 定义在详细信息中显示的字段 可以是列表 元组
    list_display = ('name', 'create_time', 'status', 'article_count')

    # 也可以由fieldsets 字段 来指定
    fields = ('name', 'status')

    # 在 分类页面展示 行内编辑区 PostInline 在上方定义
    # inlines = (PostInline,)

    def article_count(self, obj):
        """ 文章数目的统计 """
        return obj.article_set.count()

    # 指定在展示页面 表头信息
    article_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(object):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


@xadmin.sites.register(Article)
class ArticleAdmin(object):
    # 后端管理页面的渲染会按照模型表定义的来生成HTML元素 这是给予ModelAdmin和ModelForm的
    # 写一个我们自己的form，指定给ModelAdmin就OK了
    # form字段  PostAdminForm 在 adminforms.py 中
    form = ArticleAdminForm

    list_display = ('title', 'category', 'visit',
                    'status', 'operator')

    list_display_links = ['title', 'category']  # 在展示的字段上 添加的超链接

    list_filter = ['category']  # 过滤字段

    search_fields = ['title', 'category__name']  # 检索的字段

    actions_on_top = True  # 动作相关是否在顶部展示
    actions_on_bottom = True  # 动作相关是否在底部展示


    form_layout = (
        Fieldset(
            '基础信息',
            Row('title'),
            Row('tag', 'category',),
            Row('status', 'visit',),

        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:article_article_change', args=(obj.id,))
        )

    operator.short_description = '操作'
