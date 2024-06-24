from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db                          import models
from django.contrib.auth.models         import User

# Create your models here.
class Utilisateur(models.Model):
    STATUS_CHOICE = (('patient', 'PATIENT'), ('medecin', 'MEDECIN'), ('pharmacien', 'PHARMACIEN'),)
    user    = models.ForeignKey(User, verbose_name="", on_delete=models.CASCADE)
    mobile  = models.CharField(max_length=20, unique=True)
    status  = models.CharField(max_length=10, choices=STATUS_CHOICE, default="patient")
    preuve  = models.FileField(upload_to="health/static/documents/", max_length=255)
    deleted = models.BooleanField(default=False)
    
    def __init__(self):
        return f"{self.user.username} est un {self.status}."

    @property
    def is_pharmacien(self):
        return self.status == "pharmacien"

    @property
    def is_medecin(self):
        return self.status == "medecin"

    @property
    def is_patient(self):
        return self.status == "patient"
    
    @property
    def is_deleted(self):
        return self.deleted
    
class Archive:
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    archived_at    = models.DateTimeField(auto_now_add=True)
    archived_by    = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Archived {self.content_type.name} at {self.archived_at} by {self.archived_by.username}."
