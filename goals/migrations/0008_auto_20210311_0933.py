# Generated by Django 3.1.5 on 2021-03-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_auto_20210110_1810'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singletask',
            options={'ordering': ['-completed']},
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
