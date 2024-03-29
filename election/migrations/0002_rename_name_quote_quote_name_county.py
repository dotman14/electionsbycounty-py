# Generated by Django 4.1.4 on 2022-12-24 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='name',
            new_name='quote_name',
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_name', models.CharField(max_length=255, verbose_name='County Name')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.state')),
            ],
        ),
    ]
