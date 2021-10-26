# Generated by Django 3.2.8 on 2021-10-26 07:06

from django.db import migrations, models
import search.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to=search.models.nameFile)),
            ],
        ),
    ]
