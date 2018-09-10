# Generated by Django 2.1.1 on 2018-09-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processorModel', models.CharField(max_length=100)),
                ('processorSpeed', models.IntegerField()),
                ('ramModel', models.CharField(max_length=100)),
                ('ramSpeed', models.IntegerField()),
                ('diskType', models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD')], max_length=100)),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
    ]