# Generated by Django 4.2 on 2023-05-20 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_question_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pjk_question', to='dashboard.project'),
        ),
    ]