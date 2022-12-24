# Generated by Django 4.1.4 on 2022-12-23 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(max_length=255)),
                ('candidate_image_path', models.CharField(max_length=255, verbose_name='Path to Candidate Image')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(max_length=255)),
                ('party_color_rgb', models.CharField(max_length=255)),
                ('party_logo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_text', models.CharField(max_length=255, verbose_name='Quote Text')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('quote_date', models.CharField(max_length=50, verbose_name='Date of Quote')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, verbose_name='State Abbr.')),
                ('state_name', models.CharField(max_length=50, verbose_name='Name of State')),
            ],
        ),
        migrations.CreateModel(
            name='ElectionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('election_type', models.CharField(choices=[('presidential', 'Presidential'), ('governorship', 'Governorship')], max_length=30, verbose_name='Election Type')),
                ('date_of_election', models.IntegerField()),
                ('area_type', models.CharField(default='county', max_length=6, verbose_name='Area Type')),
                ('area_name', models.CharField(max_length=255, verbose_name='Area Name')),
                ('total_vote', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.candidate')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.party')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.state')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='candidate_party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.party'),
        ),
    ]
