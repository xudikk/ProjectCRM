# Generated by Django 4.1.7 on 2023-03-09 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_member_status_alter_member_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Kurs Turi')),
                ('mentor', models.ForeignKey(limit_choices_to={'is_student': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_mentor', to='dashboard.member')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('duration', models.CharField(default='6 oy', max_length=128, verbose_name='Kurs Davomiyligi')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course', to='dashboard.course')),
            ],
        ),
        migrations.CreateModel(
            name='GroupStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name="O'quvchi guruhga qo'shilgan sana")),
                ('end_date', models.DateField(blank=True, null=True, verbose_name="O'quvchi guruhdan chiqqan sana")),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.group')),
                ('student', models.ForeignKey(blank=True, limit_choices_to={'is_student': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.member')),
            ],
            options={
                'verbose_name': 'Guruh Talabasi',
                'verbose_name_plural': 'Talabalar',
                'unique_together': {('student', 'group')},
            },
        ),
    ]
