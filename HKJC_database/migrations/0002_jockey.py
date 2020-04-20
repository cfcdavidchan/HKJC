# Generated by Django 3.0.3 on 2020-04-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HKJC_database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jockey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the jockey's name", max_length=50)),
                ('chinese_name', models.CharField(blank=True, help_text="Enter the jockey's chinese name", max_length=50)),
                ('hkjc_id', models.CharField(help_text="Enter the jockey's hkjc id", max_length=10)),
            ],
        ),
    ]