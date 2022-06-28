# Generated by Django 4.0.5 on 2022-06-28 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('commands', models.PositiveIntegerField()),
                ('result', models.PositiveIntegerField()),
                ('duration', models.FloatField()),
            ],
            options={
                'db_table': 'executions',
            },
        ),
    ]