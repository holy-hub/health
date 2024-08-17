from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.db import models

from pharmacie.models import Pharmacie

# Create your models here.
class Utilisateur(User):
    SEX_CHOICES = (
        ('M', 'MASCULIN'),
        ('F', 'FEMININ'),
        ('BI', 'BISEXUEL'),
        ('N-G', 'NON-GENRE'),
    )
    mobile = models.CharField(max_length=20, blank=True, default="")
    sexe = models.CharField(max_length=20, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
    address = models.CharField(max_length=20, default="")
    deleted = models.BooleanField(default=False)
    image = models.FileField(upload_to="profile/", max_length=255, blank=True, default="static/adminLTE/img/avatar5.png")
    is_patient = models.BooleanField(default=True)
    is_medecin = models.BooleanField(default=False)
    is_pharmacien = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} est un.utilisateur."

    def is_state_pharmacien(self):
        return self.is_pharmacien

    def is_state_medecin(self):
        return self.is_medecin

    def is_state_patient(self):
        return self.is_patient

    def is_deleted(self):
        return self.deleted
    
    def set_medecin(self):
        self.is_patient, self.is_medecin, self.is_pharmacien = False, True, False

    def set_pharmacien(self):
        self.is_patient, self.is_medecin, self.is_pharmacien = False, False, True

    def archive(self):
        Archive.objects.create(content_object=self, archived_by=self).save()

class Patient(Utilisateur):
    profession = models.CharField(verbose_name="Profession du Patient", default="survivant", max_length=50)
    assurance_medicale = models.BooleanField(default=False)
    code_assurance = models.CharField(max_length=50, blank=True)
    personne_a_prevenir = models.CharField(max_length=50, blank=True)
    tel_personne_a_prevenir = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Patient { self.first_name }"

class Pharmacien(Utilisateur):
    preuvePharmacien = models.FileField(upload_to="Pharmacien/")
    pharmacie = models.ForeignKey(Pharmacie, verbose_name="Pharmacie", related_name="pharmacien", null=True, on_delete=models.CASCADE)
    approuverPharmacien =  models.BooleanField(default=False, verbose_name="Validation du pharmacien")
    verifierPharmacien =  models.BooleanField(default=False, verbose_name="verification du pharmacien")

    def __str__(self):
        return f"Pharmacien {self.first_name}"

    def save(self, *args, **kwargs):
        self.set_pharmacien()
        super().save(*args, **kwargs)

class Medecin(Utilisateur):
    preuveMedecin = models.FileField(upload_to='Medecin/')
    speciality = models.ForeignKey("medecin.Speciality", verbose_name="Specialite du medecin", null=True, on_delete=models.CASCADE)
    approuverMedecin = models.BooleanField(default=False, verbose_name="Validation du medecin")
    verifierMedecin = models.BooleanField(default=False, verbose_name="verification du medecin")

    def __str__(self):
        return f"Medecin {self.first_name}"

    def save(self, *args, **kwargs):
        self.set_medecin()
        super().save(*args, **kwargs)

class Archive:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Archive {self.content_type.name} at {self.archived_at.strftime('%Y, %B %d, %A')} by {self.archived_by.first_name}."
