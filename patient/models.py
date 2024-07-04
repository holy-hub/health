from datetime import datetime
from django.db import models
from authentification.models import Utilisateur
from django.core.mail import send_mail

# Create your models here.
class Appointement(models.Model):
    STATUS_CHOICE = (
        ('accepte', 'ACCEPTÉ'),
        ('refuse', 'REFUSÉ'),
        ('annule', 'ANNULÉ'),
        ('en attente', 'EN ATTENTE'),
    )
    patient = models.ForeignKey(Utilisateur, related_name='appointements_patient', verbose_name="Patient", on_delete=models.CASCADE)
    medecin = models.ForeignKey(Utilisateur, related_name='appointements_medecin', verbose_name="Medecin", on_delete=models.CASCADE)
    date_rdv = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default=STATUS_CHOICE[3])

    def __str__(self):
        return f"Mr {self.patient.user.last_name} {self.patient.user.first_name} a demandé un rendez-vous au Docteur {self.medecin.user.first_name}"

    def get_date(self):
        self.date_rdv = datetime.now() if self.status == self.STATUS_CHOICE[0] else None
        if self.date_rdv is not None:
            send_mail(
                "RENDEZ-VOUS ACCEPTÉ",
                f"  Votre rendez-vous est prévu pour le {self.date_rdv.strftime('%d %B à %Hh%M')}",
                self.medecin.user.email,
                [self.patient.user.email],
                fail_silently=False,
            )
        else:
            self.date_rdv = datetime.now()
            if self.status == self.STATUS_CHOICE[1]:
                send_mail(
                    "RENDEZ-VOUS REFUSÉ",
                    f"  Votre rendez-vous a ete refusé par le Dr {self.medecin.user.first_name} le {self.date_rdv.strftime('%d %B à %Hh%M')}.",
                    self.medecin.user.email,
                    [self.patient.user.email],
                    fail_silently=False,
                )
            elif self.status == self.STATUS_CHOICE[2]:
                send_mail(
                    "RENDEZ-VOUS ANNULÉ",
                    f"  Vous avez annulé votre rendez-vous le {self.date_rdv.strftime('%d %B à %Hh%M')}.",
                    self.medecin.user.email,
                    [self.patient.user.email],
                    fail_silently=False,
                )
        return self.date_rdv
