# Generated by Django 4.1.7 on 2023-03-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_course_group_groupstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Erkak'), (False, 'Ayol')], default=True, verbose_name='Jinsi'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]