# Create your views here.

from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import View

from ..article.models import Article
from .models import ArticleComment
from ..utils.mixin import dangerous


class CommonCommentView(View):
    """comment base class achieve some common attribute & method.  """

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """ redirect post view """

        return self.post(request, *args, **kwargs)

    def clean_data(self, key: str = 'pk', context: str = 'context') -> dict:
        """
        key: primary key id.
        context: comment context format string.
        return dict {res:bool, :pk:int, context:string}.
        """
        res = {
            'res': {
                'res': False
            },
            'form': {
                key: None,
                context: None,
            }
        }

        # 类型判定

        try:
            pk: int = int(self.kwargs.get(key))
            comment: str = str(self.request.POST.get(context)).strip()
            res['form'][key] = pk
        except ValueError:
            return res
            # logging ~
        if not 256 >= comment.__len__() >= 1:
            return res
        # 安全判定
        js_safe: bool = dangerous.js_safe(comment)
        if not js_safe:
            return res
        # 敏感词替换
        res['form'][context] = dangerous.safe_string(comment)
        # 返回结构化数据
        return res


class ArticleCommentView(CommonCommentView):
    """ 文章评论 """

    def post(self, request, *args, **kwargs) -> JsonResponse:
        res = {'status': False, 'msg': None}

        # get & check date
        data: dict = self.clean_data(key='article_id')

        # 数据错 直接返回
        if not data.get('res'):
            res['msg'] = 'Form data error!'
            return JsonResponse(res)

        article_id = data['form'].get('article_id')

        # 确定评论对象存在
        cache_article_list: list = cache.get('context:article:article:list')
        if cache_article_list and not cache_article_list.filter(id=article_id):  # 缓存查不到查MySQL
            if not Article.objects.filter(pk=article_id):  # 还查不到 error
                res['msg'] = 'Article is deleted！'
                return JsonResponse(res)

        # 创建评论对象
        try:
            ArticleComment.objects.create(**data['form']).save()
            res['status'] = True

        except Exception as e:
        # FIXME: logger(e)
            res['msg'] = f'Server error!{e}'

        return JsonResponse(res)
