# Generated by Django 2.0.1 on 2018-02-03 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='levelToFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='vipFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('functionname', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='vipLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vipname', models.CharField(max_length=100, null=True, verbose_name='vip等级名称')),
                ('description', models.CharField(max_length=300, null=True, verbose_name='vip等级说明')),
                ('vipFunctions', models.ManyToManyField(through='viplevels.levelToFunction', to='viplevels.vipFunction')),
            ],
            options={
                'verbose_name': 'vip等级',
                'verbose_name_plural': 'vip等级',
            },
        ),
        migrations.AddField(
            model_name='leveltofunction',
            name='vipfunctionid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viplevels.vipFunction'),
        ),
        migrations.AddField(
            model_name='leveltofunction',
            name='viplevelid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viplevels.vipLevel'),
        ),
    ]
