# Generated by Django 4.1.7 on 2023-03-07 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=512)),
                ('mobile', models.CharField(max_length=20)),
                ('is_expired', models.BooleanField(default=False)),
                ('tries', models.SmallIntegerField(default=0)),
                ('extra', models.JSONField(default={})),
                ('is_verified', models.BooleanField(default=False)),
                ('step', models.CharField(max_length=25)),
                ('by', models.IntegerField(choices=[(1, 'By Register'), (2, 'By Login')])),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('status', models.SmallIntegerField(choices=[(1, 'Faol emas'), (2, 'Faol'), (3, 'Mavjud emas'), (4, 'Yangi qo`shilmoqchi')], default=2)),
            ],
            options={
                'verbose_name': 'Lavozim',
                'verbose_name_plural': 'Lavozimlar',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=800, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos')),
                ('lat', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude')),
                ('lng', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude')),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_district', to='geo.district')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_region', to='geo.region')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(blank=True, max_length=30, null=True)),
                ('middlename', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('birthday', models.DateField()),
                ('gender', models.BooleanField(default=True)),
                ('is_student', models.BooleanField(default=False)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('address', models.CharField(max_length=255)),
                ('pass_serial', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Faol emas'), (2, 'Faol'), (3, 'Mavjud emas'), (4, 'Yangi qo`shilmoqchi')], default=2)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_district', to='geo.district')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='position', to='dashboard.position')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_region', to='geo.region')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Xodim va a`zo',
                'verbose_name_plural': 'Xodimlar va A`zolar',
            },
        ),
    ]
