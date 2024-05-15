# Generated by Django 5.0.6 on 2024-05-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_address', models.CharField(max_length=200)),
                ('org_phone', models.CharField(max_length=12)),
                ('org_email', models.EmailField(max_length=254)),
                ('research_goal', models.CharField(max_length=500)),
                ('relevance', models.CharField(max_length=500)),
                ('expected_results', models.CharField(max_length=2000)),
                ('status', models.CharField(choices=[('dr', 'черновик'), ('sa', 'сохранена'), ('se', 'отправлена на экспертизу')], max_length=2)),
                ('created', models.DateField(auto_now_add=True)),
                ('authors', models.ManyToManyField(to='applicants.author')),
            ],
        ),
    ]
