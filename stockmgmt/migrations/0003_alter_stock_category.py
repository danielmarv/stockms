# Generated by Django 3.2.12 on 2022-08-25 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0002_auto_20220825_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stockmgmt.category'),
            preserve_default=False,
        ),
    ]
