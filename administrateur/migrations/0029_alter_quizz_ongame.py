# Generated by Django 4.1.7 on 2023-05-01 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrateur', '0028_alter_association_idquestion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizz',
            name='onGame',
            field=models.CharField(default='False', max_length=10),
        ),
    ]
