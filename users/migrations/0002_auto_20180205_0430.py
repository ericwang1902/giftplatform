# Generated by Django 2.0.1 on 2018-02-05 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='privatearea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.privatearea'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='servicestaff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('supplier', '供应商'), ('giftcompany', '礼品公司'), ('service', '客服'), ('admin', '系统管管理员')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='viplevel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viplevels.vipLevel'),
        ),
    ]