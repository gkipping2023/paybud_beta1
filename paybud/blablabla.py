from main.models import User, Logbook
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone

# Pick a user to test with
user = User.objects.first()  # Get first user

# Set dates for previous month
today = timezone.now().date()
first_day_this_month = today.replace(day=1)
last_day_prev_month = first_day_this_month - timedelta(days=1)
first_day_prev_month = last_day_prev_month.replace(day=1)

# Get logbook entries
entries = Logbook.objects.filter(
    cmp_id=user.cmp_id,
    date__gte=first_day_prev_month,
    date__lte=last_day_prev_month
).order_by('date')

# Calculate totals
total_hours = sum(float(entry.total_decimal) for entry in entries)
total_sun = sum(float(entry.sun_decimal) for entry in entries)
total_holiday = sum(float(entry.holiday_decimal) for entry in entries)
total_libre = sum(float(entry.libre_decimal) for entry in entries)
total_sa = sum(float(entry.sa_decimal) for entry in entries)
total_incentive = sum(float(entry.incentive) for entry in entries)

# Prepare context
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

# Preview email content
html_message = render_to_string('emails/monthly_summary.html', context)
print(html_message)

# Send test email
send_mail(
    subject=f'Test: Your PayBud Monthly Summary - {first_day_prev_month.strftime("%B %Y")}',
    message=render_to_string('emails/monthly_summary.txt', context),
    from_email='noreply@ezy-labs.com',
    recipient_list=['george.kipping@hotmail.com','gkipping01@gmail.com'],
    html_message=html_message,
    fail_silently=False,
)

print("Email sent successfully!")