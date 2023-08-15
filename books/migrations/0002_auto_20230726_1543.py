# Generated by Django 3.0 on 2023-07-26 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='follow_author',
        ),
        migrations.AddField(
            model_name='book',
            name='year_published',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Год издания'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=200, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_available',
            field=models.BooleanField(default=False, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(default=None, max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
