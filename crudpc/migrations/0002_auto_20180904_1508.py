# Generated by Django 2.1.1 on 2018-09-04 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crudpc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtype', models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD')], default='HDD', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('speed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('speed', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='computer',
            name='diskType',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='processorModel',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='processorSpeed',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='ramModel',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='ramSpeed',
        ),
        migrations.AddField(
            model_name='computer',
            name='disk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crudpc.Disk'),
        ),
        migrations.AddField(
            model_name='computer',
            name='processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crudpc.Processor'),
        ),
        migrations.AddField(
            model_name='computer',
            name='ram',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crudpc.RAM'),
        ),
    ]