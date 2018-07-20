from django.contrib import admin
from .models import Information as ProjectInformation
from .models import Feedback as ProjectFeedback

# Register your models here.
admin.site.register(ProjectInformation)
admin.site.register(ProjectFeedback)
