from django.db import models
from ..utils.basemodel import BaseModel
from mdeditor.fields import MDTextField
# Create your models here


class ArticleComment(BaseModel):

    article = models.ForeignKey(to='article.Article', verbose_name='文章评论', on_delete=models.DO_NOTHING)
    context = MDTextField(max_length=512, verbose_name='评论', help_text='推荐MarkDown哦！')

    def flush_cache_keys(self) -> dict:
        self.CACHE_DICT['keys'] = {
            f'context:article:article:comment:{self.article_id}',
        }
        return self.CACHE_DICT

    def __str__(self) -> str:
        return f'comment:{self.article.title}'
