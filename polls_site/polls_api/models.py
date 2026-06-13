from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.timezone import now


class AppUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class PollQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateTimeField(null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="polls",
        null=True,
    )

    def has_expired(self):
        return self.exp_date and now() >= self.exp_date


class PollChoice(models.Model):
    question = models.ForeignKey(
        PollQuestion, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
