# Generated by Django 2.2.8 on 2019-12-17 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EveDoctrineCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='EveFitCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='EveFitting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('fitting', models.TextField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_eveonline_doctrine_manager.EveFitCategory')),
            ],
        ),
        migrations.CreateModel(
            name='EveSkillPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_skills', models.TextField(blank=True, null=True)),
                ('effective_skills', models.TextField(blank=True, null=True)),
                ('fitting', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skillplan', to='django_eveonline_doctrine_manager.EveFitting')),
            ],
        ),
        migrations.CreateModel(
            name='EveDoctrine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_eveonline_doctrine_manager.EveDoctrineCategory')),
                ('fittings', models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveFitting')),
            ],
        ),
    ]
