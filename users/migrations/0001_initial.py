# Generated by Django 2.0.1 on 2018-02-03 08:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viplevels', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('authStatus', models.BooleanField(default=False)),
                ('mobile', models.CharField(max_length=20)),
                ('gender', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('supplier', '供应商'), ('giftcompany', '礼品公司'), ('service', '客服'), ('admin', '系统管管理员')], max_length=10)),
                ('inprivatearea', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='privatearea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountlimit', models.IntegerField(default=0)),
                ('productlimit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='siteMessge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True)),
                ('content', models.CharField(max_length=500, null=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('hasread', models.BooleanField(default=False)),
                ('fromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromuser', to=settings.AUTH_USER_MODEL)),
                ('touser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='touser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suppliername', models.CharField(max_length=200)),
                ('tel', models.CharField(max_length=20)),
                ('qq', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userAuthinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgurl', models.ImageField(upload_to=users.models.user_directory_path)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='vipLevelChangeHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatetime', models.DateTimeField(auto_now_add=True)),
                ('destlevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destlevel', to='viplevels.vipLevel')),
                ('orignallevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orignallevel', to='viplevels.vipLevel')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='privatearea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.privatearea'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='servicestaff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='viplevel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viplevels.vipLevel'),
        ),
    ]
