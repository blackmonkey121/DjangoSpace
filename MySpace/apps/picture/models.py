from django.conf import settings
from django.core.cache import cache
from django.db import models
from PIL import Image as _Image
import time
import os

from ..utils.basemodel import BaseModel, VisitBaseModel, FileManager
from ..utils.storage import AdjustImageStorage, create_unique_name, write_test


class Album(VisitBaseModel):
    """FIXME： 以事件或人组织，不需要地址 ？"""

    name = models.CharField(max_length=64, verbose_name="相册名", default='No Name')
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

    img = models.ImageField(upload_to="picture/%Y/%m/%d/", default="picture/cover.jpeg", verbose_name="照片")
    thumbnail = models.CharField(max_length=256, verbose_name='缩略图地址', blank=True)
    album = models.ForeignKey(Album, verbose_name='相册', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs) -> None:
        """
        生成缩略图
        """
        THUMB_SIZE: tuple = (300, 300)
        ABS_DIR: str = os.path.join(settings.MEDIA_ROOT, 'thumb')
        file: str = create_unique_name(self.img.name, extend='png')
        save_path: str = os.path.join(ABS_DIR, file)
        thumb: _Image = _Image.open(self.img)   # 获取原图
        thumb.thumbnail(THUMB_SIZE)    # 生成缩略图
        thumb.save(save_path, 'png')
        # 存储缩略图URL
        self.thumbnail: str = os.path.join(settings.MEDIA_URL, 'thumb', file)

        super(Image, self).save(*args, **kwargs)

    def get_cache_keys(self) -> set:
        # FIXME：根据匹配规则批量刷新cache
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
