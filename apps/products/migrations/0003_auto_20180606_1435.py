# Generated by Django 2.0.1 on 2018-06-06 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180328_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='型号'),
        ),
        migrations.AddField(
            model_name='product',
            name='simple_description',
            field=models.TextField(blank=True, null=True, verbose_name='卖点'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='说明'),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='favouredprice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
