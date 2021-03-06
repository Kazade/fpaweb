from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.contrib.auth.models import User

from core.middleware import get_request

BUILD_STATUS_CHOICES = [
    ("queued", _("Queued")),
    ("building", _("Building")),
    ("complete", _("Complete")),
    ("failed", _("Failed")),
    ("cancelled", _("Cancelled")),
]

AVAILABLE_ARCHITECTURES = [
    ("i386", _("i686")),
    ("x86_64", _("x86_64")),
]

class DistroVersion(models.Model):
    distro = models.CharField(max_length=128)
    version = models.CharField(max_length=16)

    class Meta:
        unique_together = [
            ('distro', 'version')
        ]

class Repository(models.Model):
    name = models.CharField(max_length=512, unique=True, db_index=True)
    owner = models.ForeignKey(User, editable=False, related_name="repositories")
    description = models.TextField()   
    
    class Meta:
        verbose_name_plural = "repositories"

    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.pk and not self.owner_id:
            self.owner = get_request().user
            assert self.owner
        return super(Repository, self).save(*args, **kwargs)

class Package(models.Model):
    name = models.CharField(max_length=64, db_index=True) #What are the Fedora restrictions on name?
    repository = models.ForeignKey(Repository)

    current_version_number = models.CharField(max_length=8) #E.g. 1.2.234
    git_clone_url = models.CharField(max_length=1024)

    class Meta:
        unique_together = [
            ('name', 'repository')
        ]
        
class PackageVersion(models.Model):
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=512, db_index=True)
    architecture = models.CharField(max_length=10, choices=AVAILABLE_ARCHITECTURES)
    distro = models.ForeignKey(DistroVersion)
    
    status = models.CharField(max_length=512, choices=BUILD_STATUS_CHOICES, editable=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        unique_together = [
            ('package', 'version', 'architecture')
        ]

