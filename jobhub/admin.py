from django.contrib import admin
# Register your models here.

from django.apps import apps

# Get all models from the current app
app = apps.get_app_config('jobhub')
for model_name, model in app.models.items():
    admin.site.register(model)
