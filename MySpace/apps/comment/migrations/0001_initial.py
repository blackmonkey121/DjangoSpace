# Generated by Django 2.0.1 on 2020-07-13 02:33

import apps.utils.mixin
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0002_auto_20200713_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('context', mdeditor.fields.MDTextField(help_text='推荐MarkDown哦！', max_length=256, verbose_name='评论')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='article.Article', verbose_name='文章评论')),
            ],
            options={
                'abstract': False,
            },
            bases=(apps.utils.mixin.FlushCacheMixin, models.Model),
        ),
    ]