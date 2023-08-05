# Generated by Django 3.1.1 on 2020-10-08 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIStat',
            fields=[
                ('record_time', models.DateTimeField(auto_now=True, primary_key=True, serialize=False)),
                ('method', models.CharField(max_length=10)),
                ('path', models.CharField(db_index=True, max_length=255)),
                ('query', models.CharField(max_length=2000)),
                ('ip', models.GenericIPAddressField()),
            ],
            options={
                'ordering': ['-record_time', 'path'],
                'get_latest_by': ['-record_time', 'path'],
            },
        ),
    ]
