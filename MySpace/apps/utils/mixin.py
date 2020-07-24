#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import datetime
from django.core.cache import cache
from django.db.models import F
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import cache_page


def get_context(*args, **kwargs) -> dict:
    """ context 导航栏信息 """

    from ..article.models import Tag, Category
    from ..travel.models import Province

    model_list: dict[object:tuple, ...] = {
        Tag: ('id', 'name'),
        Category: ('id', 'name'),
    }

    # # 初始化 context
    context: dict[str:'QuerySet', str:list, ...] = dict()

    for model, para in model_list.items():
        cache_key: str = f'context:{model._meta.app_label}:{model._meta.model_name}:list'

        qs: 'QuerySet' = cache.get(cache_key)

        # 如果缓存未命中, 查询 然后更新缓存
        if qs is None:
            qs = model.objects.values(*para).filter(status=model.STATUS_NORMAL)
            # 更新缓存
            cache.set(cache_key, qs, 60*60)  # 1h
        # 更新context
        context.update(
            {f'{model._meta.model_name}_list': qs}
        )

    # 更新 province 和 city 实现 一次IO 得到全部数据
    cache_key: str = f'context:travel:province:list'
    province_qs: 'QuerySet' = cache.get(cache_key)
    if province_qs is None:

        province_qs: list = list()

        tmp_dict: dict = dict()
        # 主动联表查询所有用到的数据 优化SQL
        for p_id, p_name, c_id, c_name in Province.objects.values_list('id', 'name', 'city__id', 'city__name'):

            if not tmp_dict.get(str(p_id)):
                tmp_dict[str(p_id)] = list([{'id': p_id, 'name': p_name}])

            tmp_dict[str(p_id)].append({'id': c_id, 'name': c_name})

        # 封装成对象列表，方便模版语言遍历，前后不分离 需要在后端实现
        for province in tmp_dict.values():
            province[0]['city'] = province[1:]
            province_qs.append(province[0])

        # 更新缓存
        cache.set(cache_key, province_qs, 60 * 60)

    context.update({
        'province_list': province_qs
    })

    # FIXME:检查日期是否ok 应该在项目启动时检查配置
    if not isinstance(settings.DATE, tuple):
        raise TypeError('settings.DATE must be tuple.')

    date_key: str = 'context:article:article:date:list'
    date_merge: dict = cache.get(date_key)

    if not date_merge:

        start_year, start_month = settings.DATE
        tmp_date: datetime.date = datetime.date.today()
        end_year, end_month = tmp_date.year, tmp_date.month

        date_merge: dict = dict()
        general: list = list(range(1, 13))
        # 第一年
        date_merge.update(
            {start_year: [month for month in range(start_month, 13)]}
        )
        # 中间完整年份
        for year in range(start_year + 1, end_year):
            date_merge.update({year: general})
        # 最后一年
        date_merge.update({end_year: [month for month in range(1, end_month + 1)]})
        cache.set(date_key, date_merge, 30)  # 30s

    context.update(
        {'date_merge': date_merge}  # {key:[]}
    )

    return context


class NavViewMixin(object):
    """
    继承此类，默默的实现 navbar 所有信息 ，前提是对象必须在执行流程中调用`get_context_data` 方法,否则无效。
    对于不执行 `get_context_data`的情况（直接继承 View,甚至直接继承 Object 的）可以使用 `rich_render` 方法渲染。
    """

    def get_context_data(self, *args, **kwargs) -> dict:
        context: dict = dict() if not hasattr(super(), 'get_context_data') else super().get_context_data(*args, **kwargs)
        context.update(get_context())
        return context


class CacheMixin(object):
    cache_timeout: int = 60

    def get_cache_timeout(self) -> int:
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)


def rich_render(*args, **kwargs) -> render:
    """ 仅仅是将 render 方法套个壳，添加导航栏上下文数据 """
    context: dict = kwargs.get('context', None)
    if context is None:
        kwargs['context'] = context = dict()
    context.update(get_context())
    return render(*args, **kwargs)


class VisitIncrMixin(object):

    pk_url_kwarg: str = None
    model: 'model.Model' = None

    def get(self, request, *args, **kwargs) -> 'TemplateResponse':

        response = super().get(request, *args, **kwargs)
        self.handle_visited(request)
        return response

    def handle_visited(self, request, *args, **kwargs) -> None:
        """
        增加浏览
        TODO：应该先在缓存做统计，定时写入MySQL 减少io.
        TODO：注意保证原子性 和 更新缓存中与浏览量相关的字段.
        """
        increase: bool = False

        pk: str = getattr(self, 'pk_url_kwarg')
        pk: str = kwargs.get(pk) or self.kwargs.get(pk)
        if not pk:
            if hasattr(self, '_pk'):
                pk = self._pk
            else:
                raise KeyError(f'{self.__class__.__name__} must rely on a primary key flag or "_pk".')
        model: 'model.Model' = getattr(self, 'model')

        uid: str = request.uid
        visit_key: str = f'visit:{uid}:{self.request.path}'

        if not cache.get(visit_key):
            increase = True
            cache.set(visit_key, 1, 5 * 60)  # 5分钟

        if increase:
            # self.object.update(visit=F('visit') + 1)
            ret: int = model.objects.filter(pk=pk).update(visit=F('visit') + 1)

            if not ret:
                # TODO: 查询了不存在的资源，判断是否是恶意请求。
                pass


class DangerousString(object):

    def safe_string(self, string: str) -> str:
        """ 敏感词检测
        @type string: object
        """
        return string

    def js_safe(self, string: str) -> bool:

        return True

dangerous = DangerousString()
