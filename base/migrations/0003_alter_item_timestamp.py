# Generated by Django 4.1.5 on 2023-02-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_item_msg_direction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='timestamp',
            field=models.DateTimeField(null=True, verbose_name='생성일시'),
        ),
    ]
