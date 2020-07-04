#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import datetime

from django.conf import settings
from django.core.cache import cache


def get_context(*args, **kwargs):
    # context 待查询的模型 和 对应的字段信息

    from ..article.models import Tag, Category
    from ..travel.models import Province

    model_list: dict[object:tuple, ...] = {
        Tag: ('id', 'name'),
        Category: ('id', 'name'),
    }

    # # 初始化 context
    context: dict[str:'queryset', str:list, ...] = dict()

    for model, para in model_list.items():
        cache_key: str = 'context:%s:list' % model.__name__.lower()

        model_values = cache.get(cache_key)

        # 如果缓存未命中, 查询 然后更新缓存
        if model_values is None:
            model_values = model.objects.values(*para).filter(status=model.STATUS_NORMAL)

            # 更新缓存
            cache.set(cache_key, model_values, 24 * 3600)  # 24h

        # 更新context
        context.update(
            {'%s_list' % model.__name__.lower(): model_values}
        )

    # 更新 province 和 city 实现 一次IO 得到全部数据
    cache_key = 'context:%s:list' % Province.__name__.lower()
    province_list = cache.get(cache_key)
    if province_list is None:

        province_list = list()

        tmp_dict = dict()
        # 主动联表查询所有用到的数据 优化SQL
        for p_id, p_name, c_id, c_name in Province.objects.values_list('id', 'name', 'city__id', 'city__name'):

            if not tmp_dict.get(str(p_id)):
                tmp_dict[str(p_id)] = list([{'id': p_id, 'name':p_name}])

            tmp_dict[str(p_id)].append({'id': c_id, 'name': c_name})

        # 封装成对象列表，方便模版语言遍历，前后不分离 需要在后端实现
        for province in tmp_dict.values():
            province[0]['city'] = province[1:]
            province_list.append(province[0])

        # 更新缓存
        cache.set(cache_key, province_list, 24 * 3600)

    context.update({
        'province_list': province_list
    })

    # FIXME:检查日期是否ok 应该在项目启动时检查配置
    if not isinstance(settings.DATE, tuple):
        raise TypeError('settings.DATE must be tuple.')

    date_key = 'context:date_merge'
    date_merge = cache.get(date_key)

    if not date_merge:

        start_year, start_month = settings.DATE
        tmp_date = datetime.date.today()
        end_year, end_month = tmp_date.year, tmp_date.month

        date_merge: dict = dict()
        general: list = list(range(1, 13))

        date_merge.update({start_year: [month for month in range(start_month, 13)]})
        for year in range(start_year + 1, end_year):
            date_merge.update({year: general})
        date_merge.update({end_year: [month for month in range(1, end_month + 1)]})

        cache.set(date_key, date_merge, 30)  # 30s

    context.update(
        {'date_merge': date_merge}  # {key:[]}
    )

    return context


class CacheMap(object):

    article = {
        'category': [
            'context:category:list',
        ],

        'tag': [
            'context:tag:list',
        ]

    }

    life = {

    }

    picture = {
        'album': [
            'context:album:list',
            ''
        ],
        'image': [
            'context:album:list',
            'context:image:list'
        ],

    }

    travel = {
        'province': [
            'context:province:list'
        ]

    }

    @classmethod
    def delete(cls, model=None):
        """  """

        map = getattr(cls, model._meta.app_label)
        cache_list = map.get(model._meta.model_name, None)

        print(cache_list)

        if cache_list:
            for cache_name in cache_list:
                cache.delete(cache_name)
