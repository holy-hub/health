import random
from django.utils import timezone
from django.db import models
from authentification.models import Patient, Medecin
from django.core.mail import send_mail

# Create your models here.
class Appointement(models.Model):
    STATUS_CHOICE = (
        ('accepte', 'ACCEPTÉ'),
        ('refuse', 'REFUSÉ'),
        ('annule', 'ANNULÉ'),
        ('en attente', 'EN ATTENTE'),
    )
    patient = models.ForeignKey(Patient, related_name='appointements_patient', verbose_name="Patient", on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, related_name='appointements_medecin', verbose_name="Medecin", on_delete=models.CASCADE)
    date_rdv = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default=STATUS_CHOICE[3])
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Mr {self.patient.last_name} {self.patient.first_name} a demandé un rendez-vous au Docteur {self.medecin.first_name}"

    def response(self, n):
        if 0 <= n >= 3:
            self.status = self.STATUS_CHOICE[n]
            self.action()

    def action(self):
        self.date_rdv = timezone.now() if self.status == self.STATUS_CHOICE[0] else None
        if self.date_rdv is not None:
            self.send_reminder_email()
            self.reminder_sent = True
            send_mail(
                "RENDEZ-VOUS ACCEPTÉ",
                f"  Votre rendez-vous est prévu pour le {self.date_rdv.strftime('%d %B à %Hh%M')}",
                self.medecin.email,
                [self.patient.email],
                fail_silently=False,
            )
        else:
            self.date_rdv = timezone.now()
            if self.status == self.STATUS_CHOICE[1]:
                send_mail(
                    "RENDEZ-VOUS REFUSÉ",
                    f"  Votre rendez-vous a ete refusé par le Dr {self.medecin.first_name} le {self.date_rdv.strftime('%d %B à %Hh%M')}.",
                    self.medecin.email,
                    [self.patient.email],
                    fail_silently=False,
                )
            elif self.status == self.STATUS_CHOICE[2]:
                send_mail(
                    "RENDEZ-VOUS ANNULÉ",
                    f"  Vous avez annulé votre rendez-vous le {self.date_rdv.strftime('%d %B à %Hh%M')}.",
                    self.medecin.email,
                    [self.patient.email],
                    fail_silently=False,
                )
        return self.date_rdv

    def send_reminder_email(self):
        messages = [
            f'Bonjour {self.patient.first_name}, ceci est un rappel pour votre rendez-vous prévu le {self.date_rdv.strftime("%d %B à %Hh%Mmin")}.',
            f'Bonjour {self.patient.first_name}, votre rendez-vous est prévu pour le {self.date_rdv.strftime("%d %B à %Hh%M")}.'
        ]
        msg = random.choice(messages)
        try:
            send_mail(
                "RAPPEL DE RENDEZ-VOUS",
                msg,
                self.medecin.email,
                [self.patient.email],
                fail_silently=False,
            )
            print(f"Email de rappel envoyé avec succès à {self.patient.email}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email de rappel: {e}")
