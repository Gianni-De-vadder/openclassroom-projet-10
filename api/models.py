from django.db import models
from accounts.models import User


from django.db import models
from accounts.models import User


class Contributors(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contributions"
    )
    project = models.ForeignKey(
        "Projects", on_delete=models.CASCADE, related_name="project_contributors"
    )
    permission = models.CharField(max_length=10, blank=True)
    role = models.CharField(max_length=255)

    objects = models.Manager()


class ProjectType(models.TextChoices):
    FEATURE = "Feature", "Feature"
    BUG = "Bug", "Bug"
    ENHANCEMENT = "Enhancement", "Enhancement"
    TASK = "Task", "Task"
    OTHER = "Other", "Other"


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ProjectType.choices)
    author_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )
    contributors = models.ManyToManyField(
        User, through="Contributors", related_name="contributed_projects"
    )

    objects = models.Manager()


class Priority(models.TextChoices):
    Low = "LOW", "Faible"
    Medium = "MED", "Moyen"
    High = "HIGH", "Haute"


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255, choices=Priority.choices)
    status = models.CharField(max_length=255)
    author_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="issues"
    )
    assignee_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_issues"
    )
    created_time = models.DateTimeField()

    objects = models.Manager()


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    author_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    issue_id = models.ForeignKey(
        Issues, on_delete=models.CASCADE, related_name="comments"
    )
    created_time = models.DateTimeField()

    objects = models.Manager()
