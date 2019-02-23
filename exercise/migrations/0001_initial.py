# Generated by Django 2.1.7 on 2019-02-23 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=8)),
                ('destination', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='exchangetype',
            unique_together={('origin', 'destination')},
        ),
        migrations.AddField(
            model_name='exchangerate',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.ExchangeType'),
        ),
        migrations.AlterUniqueTogether(
            name='exchangerate',
            unique_together={('date', 'currency')},
        ),
    ]