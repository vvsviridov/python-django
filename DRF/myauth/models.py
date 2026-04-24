from django.db import models
from django.contrib.auth.models import User


def profile_avatar_dir_path(instance: "User", filename: str) -> str:
    return "profile/{pk}/avatar/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=profile_avatar_dir_path, null=True, blank=True)
