# Generated by Django 2.0.1 on 2020-07-02 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('cover', models.ImageField(blank=True, upload_to='upload', verbose_name='封面')),
                ('name', models.CharField(max_length=32, verbose_name='城市名')),
                ('desc', models.CharField(max_length=256, verbose_name='描述')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='ImageManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('visit', models.SmallIntegerField(default=0, verbose_name='浏览量')),
                ('desc', models.CharField(max_length=256, verbose_name='描述')),
                ('img', models.FileField(default='travel/cover.jpeg', upload_to='travel/', verbose_name='头像')),
            ],
            options={
                'verbose_name': '照片',
                'verbose_name_plural': '照片',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('title', models.CharField(default='No Title', max_length=32, verbose_name='景点名')),
                ('context', models.CharField(default='添加记录', max_length=256, verbose_name='记录')),
                ('addr', models.CharField(max_length=128, verbose_name='地点')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.City', verbose_name='城市')),
            ],
            options={
                'verbose_name': '景点',
                'verbose_name_plural': '景点',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('cover', models.FileField(default='travel/cover.jpeg', upload_to='travel', verbose_name='封面')),
                ('name', models.CharField(max_length=32, verbose_name='省')),
                ('desc', models.CharField(max_length=256, verbose_name='描述')),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '发布'), (0, '删除'), (2, '待发布')], default=1, verbose_name='状态')),
                ('visit', models.SmallIntegerField(default=0, verbose_name='浏览量')),
                ('title', models.CharField(max_length=64, verbose_name='旅程')),
                ('context', models.CharField(max_length=1024, verbose_name='描述')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.Province', verbose_name='省份')),
            ],
            options={
                'verbose_name': '旅程',
                'verbose_name_plural': '旅程',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='point',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.Travel', verbose_name='旅行'),
        ),
        migrations.AddField(
            model_name='imagemanager',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.Point', verbose_name='景点'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.Province', verbose_name='省份'),
        ),
    ]
