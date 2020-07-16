from django.core.cache import cache
from django.db import models
from ..utils.basemodel import BaseModel, VisitBaseModel, FileManager
from ..utils.storage import AdjustImageStorage


class Album(VisitBaseModel):
    """FIXME： 以事件或人组织，不需要地址 ？"""

    name = models.CharField(max_length=64, verbose_name="相册名", default='No Name', db_index=True)
    desc = models.CharField(max_length=512, verbose_name='描述')
    cover = models.ImageField(upload_to="picture/%Y/%m/%d/", verbose_name="封面", blank=True)

    def get_cache_keys(self) -> set:

        ret_set: set = {
            f'context:{self._meta.app_label}:{self._meta.model_name}:list',
        }
        return ret_set

    def save(self, *args, **kwargs) -> None:
        """
        # 调整图像,保存封面缩略图
        FIXME：后期可能回添加其他处理 实现 Storage 实例
        """

        self.cover.field.storage = AdjustImageStorage(re_size=(240, 240))
        super(Album, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "相册"
        ordering = ['-id', ]   # 按照id降序排列


class Image(FileManager):

    img = models.FileField(upload_to="picture/%Y/%m/%d/", default="picture/cover.jpeg", verbose_name="照片")
    album = models.ForeignKey(Album, verbose_name='相册', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs) -> None:
        """
        FIXME: 调整照片大小
        TODO: 水印在全局的 File 存储上实现～ ～ 简直有病～ @！改
        """
        super().save(*args, **kwargs)

    def get_cache_list(self) -> set:
        ret_set: set = {
            f'context:{self._meta.app_label}:{self.album._meta.model_name}:list',  # 相册有照片数量，要更新
            f'context:{self._meta.app_label}:{self._meta.model_name}:list:by:{self.album._meta.model_name}:{self.album.id}',
        }
        return ret_set

    def __str__(self) -> str:
        return '%s(%s)' % (self.album.name, self.id)

    class Meta:
        verbose_name = verbose_name_plural = "照片"
        ordering = ['-id', ]   # 按照id降序排列
