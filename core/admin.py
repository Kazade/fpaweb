from django.contrib import admin
from core.models import Repository

class RepositoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

admin.site.register(Repository, RepositoryAdmin)
