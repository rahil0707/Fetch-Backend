# Generated by Django 5.1.1 on 2024-09-26 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer', models.CharField(max_length=256)),
                ('points', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]
