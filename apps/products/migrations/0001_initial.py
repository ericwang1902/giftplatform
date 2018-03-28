# Generated by Django 2.0.1 on 2018-03-28 15:20

import apps.products.models
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='brands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to=apps.products.models.brand_directory_path)),
                ('isdelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isroot', models.BooleanField(default=False)),
                ('isleaf', models.BooleanField(default=False)),
                ('isdelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=200, verbose_name='说明')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=0)),
                ('isdelete', models.BooleanField(default=False)),
                ('attributes', django_mysql.models.JSONField(default=dict)),
                ('yijiandaifa', models.BooleanField(default=False)),
                ('newup', models.BooleanField(default=False)),
                ('inprivatearea', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='productImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productimage', models.ImageField(upload_to=apps.products.models.product_directory_path)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='productItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('attributes', django_mysql.models.JSONField(default=dict)),
                ('status', models.IntegerField(default=0)),
                ('onshell', models.BooleanField(default=False)),
                ('favouredprice', models.DecimalField(decimal_places=2, default=0, max_digits=2)),
                ('isdelete', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productItems', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='productimage',
            name='product_item_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.productItem'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='productid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product'),
        ),
    ]
