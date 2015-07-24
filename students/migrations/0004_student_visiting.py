# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_student_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_visiting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visiting', models.IntegerField(max_length=5, null=True, blank=True)),
                ('student_name', models.ForeignKey(verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student', null=True)),
            ],
            options={
                'verbose_name': '\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u043d\u044f',
            },
            bases=(models.Model,),
        ),
    ]
