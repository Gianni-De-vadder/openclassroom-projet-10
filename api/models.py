from django.db import models
from accounts.models import User


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.IntegerField()
    role = models.CharField(max_length=255)

    objects = models.Manager()


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    project_id = models.IntegerField()
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )

    objects = models.Manager()


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="issues"
    )
    assignee_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_issues"
    )
    created_time = models.DateTimeField()

    objects = models.Manager()


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    issue_id = models.ForeignKey(
        Issues, on_delete=models.CASCADE, related_name="comments"
    )
    created_time = models.DateTimeField()

    objects = models.Manager()
