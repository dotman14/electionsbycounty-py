# Generated by Django 4.1.4 on 2022-12-28 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0004_electiondata_total_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electiondata',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='election.candidate'),
        ),
        migrations.AlterField(
            model_name='electiondata',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='election.party'),
        ),
    ]
