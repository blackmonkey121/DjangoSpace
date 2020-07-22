#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

cache = {}

THUMB_SIZE: tuple = (300, 300)
file: str = os.path.split(self.img.path)[-1]
file: str = create_unique_name(file, extend='png').replace(' ', '_')
relative_path: str = str(os.path.join(settings.MEDIA_URL, 'thumb', file))
abstract_path: str = str(os.path.join(settings.MEDIA_ROOT, 'thumb', file))

thumb: _Image.Image = _Image.open(self.img)
rn = thumb.thumbnail(THUMB_SIZE)
print(rn)
thumb.save('hello.png')
# write_test(abstract_path)
# thumb.


thumb.save(relative_path, 'PNG')
print(relative_path, abstract_path)
# thumb.seek(0)
self.thumbnail = relative_path

super().save(*args, **kwargs)