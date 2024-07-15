from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Utilisateur(User):
    SEX_CHOICES = (
        ('M', 'MASCULIN'),
        ('F', 'FEMININ'),
        ('BI', 'BISEXUEL'),
        ('N-G', 'NON-GENRE'),
    )
    STATUS_CHOICE = (('patient', 'PATIENT'), ('medecin', 'MEDECIN'), ('pharmacien', 'PHARMACIEN'))
    mobile = models.CharField(max_length=20, unique=True)
    sexe = models.CharField(max_length=20, choices=SEX_CHOICES, default=SEX_CHOICES[0])
    address = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default=STATUS_CHOICE[0])
    deleted = models.BooleanField(default=False)
    image = models.FileField(upload_to="static/adminLTE/img/profile/", max_length=255, blank=True, default="static/adminLTE/img/avatar5.png")

    def __str__(self):
        return f"{self.first_name} est un {self.status}."

    def is_pharmacien(self):
        return self.status == self.STATUS_CHOICE[2]

    def is_medecin(self):
        return self.status == self.STATUS_CHOICE[1]

    def is_patient(self):
        return self.status == self.STATUS_CHOICE[0]

    def is_deleted(self):
        return self.deleted
    
    def set_mededecin(self):
        self.status = self.STATUS_CHOICE[1]

    def set_pharmacien(self):
        self.status = self.STATUS_CHOICE[2]

    def archive(self):
        Archive.objects.create(content_object=self, archived_by=self).save()

class Pharmacien(Utilisateur):
    preuvePharmacien = models.FileField(upload_to="health/static/Pharmacien/")
    pharmacie = models.ForeignKey('pharmacie.Pharmacie', verbose_name="Pharmacie", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pharmacien {self.first_name}"

    def save(self, *args, **kwargs):
        self.status = self.STATUS_CHOICE[2]
        super().save(*args, **kwargs)

class Medecin(Utilisateur):
    preuveMedecin = models.FileField(upload_to='health/static/Medecin/')
    speciality = models.ForeignKey("medecin.Speciality", verbose_name="Specialite du medecin", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Medecin {self.first_name}"

    def save(self, *args, **kwargs):
        self.status = self.STATUS_CHOICE[1]
        super().save(*args, **kwargs)

class Patient(Utilisateur):
    profession = models.CharField(verbose_name="Profession du Patient", default="survivant", max_length=50)
    assurance_medicale = models.BooleanField(default=False)
    code_assurance = models.CharField(max_length=50, blank=True)
    personne_a_prevenir = models.CharField(max_length=50, blank=True)
    tel_personne_a_prevenir = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Patient { self.first_name }"

class Archive:
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Archive {self.content_type.name} at {self.archived_at.strftime('%Y, %B %d, %A')} by {self.archived_by.first_name}."

    