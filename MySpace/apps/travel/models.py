from django.db import models
from django.core.cache import cache
# Create your models here.

from ..utils.basemodel import BaseModel, VisitBaseModel, FileManager


class Travel(VisitBaseModel):

    cache_list: list = [
        'context:province:list',
    ]

    title = models.CharField(max_length=64, blank=False, verbose_name="旅程")
    context = models.CharField(max_length=1024, blank=False, verbose_name='描述')
    province = models.ForeignKey(to='Province', blank=False, verbose_name='省份', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = verbose_name_plural = "旅程"
        ordering = ['-id', ]   # 按照id降序排列

    def __str__(self):
        return self.title


class Province(BaseModel):
    cover = models.FileField(upload_to="travel/%Y/%m/%d/", default="travel/cover.jpeg", verbose_name="封面")
    name = models.CharField(max_length=32, verbose_name='省')
    desc = models.CharField(max_length=256, verbose_name='描述')

    def save(self, *args, **kwargs) -> None:
        """ 更新缓存 """
        cache_key = 'context:%s:list' % self.__class__.__name__.lower()
        cache.delete(cache_key)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "省份"
        ordering = ['-id', ]   # 按照id降序排列


class City(BaseModel):

    cover = models.ImageField(upload_to="travel/%Y/%m/%d/", verbose_name="封面", blank=True)
    name = models.CharField(max_length=32, verbose_name='城市名')
    desc = models.CharField(max_length=256, verbose_name='描述')
    province = models.ForeignKey(Province, blank=False, verbose_name='省份', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = verbose_name_plural = '城市'

    def __str__(self) -> str:
        return self.name


class Point(BaseModel):
    title = models.CharField(max_length=32, default='No Title', verbose_name='景点名')
    context = models.CharField(max_length=256, default='添加记录', verbose_name='记录')
    addr = models.CharField(max_length=128, blank=False, verbose_name='地点')
    travel = models.ForeignKey(to='Travel', blank=False, verbose_name='旅行', on_delete=models.DO_NOTHING)
    city = models.ForeignKey(to='City', blank=False, verbose_name='城市', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "景点"
        ordering = ['-id', ]   # 按照id降序排列


class ImageManager(FileManager):
    desc = models.CharField(max_length=256, verbose_name='描述')
    img = models.FileField(upload_to="travel/%Y/%m/%d/", default="travel/cover.jpeg", verbose_name="头像")
    point = models.ForeignKey(Point, verbose_name='景点', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = verbose_name_plural = "照片"
        ordering = ['-id', ]   # 按照id降序排列

    def __str__(self) -> str:
        return 'Point:%s image %s date %s' % (self.point, self.id, self.create_time)
