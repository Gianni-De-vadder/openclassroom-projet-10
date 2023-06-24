# Generated by Django 4.2.1 on 2023-06-24 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_rename_author_user_id_projects_author_user_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="issues",
            old_name="author_user_id",
            new_name="author_user",
        ),
        migrations.AlterField(
            model_name="contributors",
            name="permission",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="issues",
            name="tag",
            field=models.CharField(
                choices=[("LOW", "Faible"), ("MED", "Moyen"), ("HIGH", "Haute")],
                max_length=255,
            ),
        ),
    ]