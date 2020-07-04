#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from io import BytesIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class BaseStorage(FileSystemStorage):

    @staticmethod
    def convert_image_to_file(image, name):
        """ 将处理完的图片对象'Image.Image'转化为 `InMemoryUploadedFile` """
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)


class WatermarkStorage(BaseStorage):

    def save(self, name, content, max_length=None):

        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content)
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    def watermark_with_text(self, file_obj, fontfamily=None):

        text = 'blackmonkey.cn' if not hasattr(settings, 'WATER_TEXT') else settings.WATER_TEXT

        color = 'deepskyblue' if not hasattr(settings, 'WATER_COLOR') else settings.WATER_COLOR

        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 3  # 计算横轴位置
        y = height - textHeight - margin  # 计算纵轴位置
        draw.text((x, y), text, color, font)

        return image


class AdjustImageStorage(BaseStorage):
    """  """

    def __init__(self, re_size=None, *args, **kwargs,  ):
        self.re_size = re_size or (300, 300)
        super(AdjustImageStorage, self).__init__(*args, **kwargs)

    def save(self, name: str, content: InMemoryUploadedFile, max_length: int = None) -> object:

        if 'image' in content.content_type:
            image = self.adjust_size(content)
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    def adjust_size(self, content: InMemoryUploadedFile, *args, **kwargs) -> 'Image.Image':
        """ 调整上传图片的大小 """
        image = Image.open(content)
        width, height = image.size

        offset = abs(height - width) // 2
        if height > width:
            plat = (0, offset, width, height - offset,)
        else:
            plat = (offset, 0, width - offset, height)
        image = image.crop(plat)
        image = image.resize(self.re_size)
        return image
