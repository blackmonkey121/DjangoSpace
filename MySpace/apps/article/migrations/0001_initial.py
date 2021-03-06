# Generated by Django 2.0.1 on 2020-07-02 20:35

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('visit', models.SmallIntegerField(default=0, verbose_name='浏览量')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('desc', models.CharField(max_length=512, verbose_name='摘要')),
                ('content', mdeditor.fields.MDTextField(help_text='MarkDown格式', verbose_name='正文')),
                ('content_html', models.TextField(blank=True, editable=False, verbose_name='正文html')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='article.Category', verbose_name='文章分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='article.Tag', verbose_name='标签'),
        ),
    ]
