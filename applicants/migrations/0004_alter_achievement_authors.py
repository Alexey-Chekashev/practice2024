# Generated by Django 5.0.6 on 2024-05-16 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_alter_author_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='authors',
            field=models.ManyToManyField(blank=True, null=True, to='applicants.author'),
        ),
    ]
