# Generated by Django 4.1.5 on 2023-02-20 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_name_alter_user_userid'),
        ('variables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variables',
            name='baselined',
            field=models.IntegerField(default=0, verbose_name='요금적용전력'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variables',
            name='contracted',
            field=models.IntegerField(default=0, verbose_name='기본계약전력'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variables',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='관리자아이디'),
        ),
    ]
