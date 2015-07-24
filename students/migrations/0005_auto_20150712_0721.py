# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_student_visiting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_visiting',
            name='student_name',
            field=models.OneToOneField(null=True, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student'),
            preserve_default=True,
        ),
    ]
