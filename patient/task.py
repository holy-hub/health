from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Appointement

"""
@shared_task
def send_appointment_reminders():
    now = timezone.now()
    upcoming_appointments = Appointement.objects.filter(date_rdv__gte=now, date_rdv__lte=now + timezone.timedelta(hours=24))

    for appointment in upcoming_appointments:
        send_mail(
            'Rappel de rendez-vous',
            f'Bonjour {appointment.patient.first_name}, ceci est un rappel pour votre rendez-vous prévu le {appointment.date_rdv.strftime('%d %B à %Hh%Mmin')}.',
            'health@healthy.com',
            [appointment.patient.email],
            fail_silently=False,
        )
"""
@shared_task
def send_appointment_reminders():
    appointments = Appointement.objects.filter(date_rdv__gt=timezone.now(), reminder_sent=False)
    for appointment in appointments:
        appointment.send_reminder_email()
    return f"{len(appointments)} rappels envoyés."