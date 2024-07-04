from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from pharmacie.models import Pharmacie
from medecin.models import SubSpeciality
from django.db import models

# Create your models here.
class Utilisateur(models.Model):
    STATUS_CHOICE = (('patient', 'PATIENT'), ('medecin', 'MEDECIN'), ('pharmacien', 'PHARMACIEN'),)
    user = models.ForeignKey(User, verbose_name="", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default=STATUS_CHOICE[0])
    preuve = models.FileField(upload_to="health/static/documents/", max_length=255)
    deleted = models.BooleanField(default=False)

    subSpeciality = models.ForeignKey('medecin.SubSpeciality', verbose_name="Specialite du medecin", null=True, on_delete=models.CASCADE)
    pharmacie = models.ForeignKey('pharmacie.Pharmacie', verbose_name="Pharmacie", null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} est un {self.status}."

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_CHOICE[2]:
            self.subSpeciality, _ = SubSpeciality.objects.get_or_create(nom=self.speciality)
        elif self.status == self.STATUS_CHOICE[1]:
            self.subSpeciality, _ = SubSpeciality.objects.get_or_create(nom="Pharmacien")
            self.pharmacie, _ = Pharmacie.objects.get_or_create(nom=self.pharmacie)
        else:
            self.subSpeciality, _ = SubSpeciality.objects.get_or_create(nom="Patient")
        super().save(*args, **kwargs)

    def is_pharmacien(self):
        return self.status == self.STATUS_CHOICE[2]

    def is_medecin(self):
        return self.status == self.STATUS_CHOICE[1]

    def is_patient(self):
        return self.status == self.STATUS_CHOICE[0]

    def is_deleted(self):
        return self.deleted

    def archive(self):
        Archive.objects.create(content_object=self, archived_by=self).save()

    def my_pharmacie(self):
        if self.is_pharmacien:
            return Pharmacie.objects.filter(pharmacien=self).order_by('created_at').all()
        return []

class Archive:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Archived {self.content_type.name} at {self.archived_at} by {self.archived_by.username}."
