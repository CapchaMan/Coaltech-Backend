# migration for custom user
from django.db import migrations, models
import django.utils.timezone
import django.contrib.auth.models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth','0001_initial'),
        ('contenttypes','0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('role', models.CharField(choices=[('user','User'),('vendor','Vendor'),('rider','Rider')], default='user', max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={'abstract': False,},
            managers=[('objects', django.contrib.auth.models.UserManager()),],
        ),
    ]
