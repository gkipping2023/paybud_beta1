from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from main.models import User, Logbook
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send monthly logbook summaries to users on the 5th of each month'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sending summaries regardless of the date',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        force = options.get('force', False)
        
        # Only run on the 5th of the month (unless --force is used)
        if not force and today.day != 5:
            self.stdout.write(
                self.style.WARNING(f'Today is the {today.day}th. This command runs on the 5th of each month.')
            )
            return

        # Get previous month
        first_day_this_month = today.replace(day=1)
        last_day_prev_month = first_day_this_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)

        self.stdout.write(f'Generating summaries for {first_day_prev_month.strftime("%B %Y")}...')

        # Get all users with email addresses
        users = User.objects.filter(email__isnull=False).exclude(email='')

        sent_count = 0
        for user in users:
            try:
                # Get logbook entries for the previous month
                entries = Logbook.objects.filter(
                    cmp_id=user.cmp_id,
                    date__gte=first_day_prev_month,
                    date__lte=last_day_prev_month
                ).order_by('date')

                if not entries.exists():
                    continue

                # Calculate totals (handle None values)
                total_hours = sum(float(entry.total_decimal or 0) for entry in entries)
                total_sun = sum(float(entry.sun_decimal or 0) for entry in entries)
                total_holiday = sum(float(entry.holiday_decimal or 0) for entry in entries)
                total_libre = sum(float(entry.libre_decimal or 0) for entry in entries)
                total_sa = sum(float(entry.sa_decimal or 0) for entry in entries)
                total_incentive = sum(float(entry.incentive or 0) for entry in entries)

                # Prepare context for email template
                context = {
                    'user': user,
                    'month': first_day_prev_month.strftime('%B %Y'),
                    'entries': entries,
                    'totals': {
                        'hours': round(total_hours, 2),
                        'sun': round(total_sun, 2),
                        'holiday': round(total_holiday, 2),
                        'libre': round(total_libre, 2),
                        'sa': round(total_sa, 2),
                        'incentive': round(total_incentive, 2),
                    },
                    'entry_count': entries.count(),
                }

                # Render email template
                subject = f'Your PayBud Monthly Summary - {first_day_prev_month.strftime("%B %Y")}'
                html_message = render_to_string('emails/monthly_summary.html', context)
                text_message = render_to_string('emails/monthly_summary.txt', context)

                # Send email
                send_mail(
                    subject=subject,
                    message=text_message,
                    from_email='noreply@paybud.com',
                    recipient_list=[user.email],
                    #recipient_list=['george.kipping@hotmail.com','gkipping01@gmail.com'],  # For testing purposes
                    html_message=html_message,
                    fail_silently=False,
                )

                sent_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Sent summary to {user.email}')
                )

            except Exception as e:
                logger.error(f'Error sending summary to {user.cmp_id} ({user.email}): {str(e)}')
                self.stdout.write(
                    self.style.ERROR(f'✗ Error sending to {user.email}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully sent {sent_count} monthly summaries!')
        )
