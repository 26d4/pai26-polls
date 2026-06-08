from django.contrib import admin
from . import models

admin.site.register(models.AppUser)
admin.site.register(models.PollQuestion)
admin.site.register(models.PollChoice)
