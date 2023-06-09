# Generated by Django 4.2.1 on 2023-06-16 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projects",
            old_name="author_user_id",
            new_name="author_user",
        ),
        migrations.RemoveField(
            model_name="contributors",
            name="project_id",
        ),
        migrations.RemoveField(
            model_name="contributors",
            name="user_id",
        ),
        migrations.RemoveField(
            model_name="projects",
            name="project_id",
        ),
        migrations.AddField(
            model_name="contributors",
            name="project",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_contributors",
                to="api.projects",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contributors",
            name="user",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributions",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projects",
            name="contributors",
            field=models.ManyToManyField(
                related_name="contributed_projects",
                through="api.Contributors",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
