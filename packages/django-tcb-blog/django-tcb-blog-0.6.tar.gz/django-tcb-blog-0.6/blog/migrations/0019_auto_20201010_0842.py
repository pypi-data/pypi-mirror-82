# Generated by Django 3.0.3 on 2020-10-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20201009_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='entryenvelope',
            name='tags',
            field=models.ManyToManyField(related_name='entries', to='blog.Tag'),
        ),
    ]
