# Monthly Summary Email Feature - Setup Guide

This feature sends monthly summaries of logbook entries to users on the 5th of each month.

## Overview

- **Command**: `python manage.py send_monthly_summary`
- **Frequency**: Runs daily (scheduled on PythonAnywhere), but only executes on the 5th of each month
- **Email Backend**: Mailgun (production) / SMTP (development)
- **Template**: HTML and plain text emails

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** in your `.env` file or PythonAnywhere web app settings:

   **For Mailgun (Production)**:
   ```
   ENVIRONMENT=production
   MAILGUN_API_KEY=your-mailgun-api-key
   MAILGUN_SENDER_DOMAIN=mg.paybud.com
   DEFAULT_FROM_EMAIL=noreply@paybud.com
   ```

   **For SMTP (Local Development)**:
   ```
   ENVIRONMENT=local
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-password
   ```

3. **Run migrations** (if you haven't already):
   ```bash
   python manage.py migrate
   ```

## Setting up PythonAnywhere Scheduled Task

### Steps:

1. Log in to your PythonAnywhere account
2. Go to **Web** tab → Select your web app
3. Click on **Tasks** (or **Scheduled Tasks** depending on your plan)
4. Click **Create a new scheduled task**
5. **Set the time**: Choose **05:00** (5 AM UTC) - this ensures it runs around the 5th of each month
6. **Command**:
   ```
   /home/yourusername/paybud_beta1/venv/bin/python /home/yourusername/paybud_beta1/manage.py send_monthly_summary
   ```
   
   Replace `yourusername` with your actual PythonAnywhere username.

7. **Schedule**: Set to run **Daily** - the script will automatically check if it's the 5th of the month

### Example Task Configuration:
```
Time: 05:00
Frequency: Daily
Command: /home/george/paybud_beta1/venv/bin/python /home/george/paybud_beta1/manage.py send_monthly_summary
```

## How It Works

1. **Triggers on the 5th**: The command checks if today is the 5th of the month
2. **Fetches data**: Retrieves all logbook entries from the previous month for each user
3. **Calculates totals**: 
   - Total flight hours
   - Sun hours, Holiday hours, Libre hours, SA hours
   - Incentive amount
4. **Sends email**: Uses the configured email backend to send a formatted summary
5. **Logging**: Outputs success/error messages for monitoring

## Email Content

The email includes:
- User name and month
- Monthly totals (flight hours by category)
- List of all entries for that month
- Total incentive earned
- Link to log in for more details

Templates:
- **HTML**: `templates/emails/monthly_summary.html`
- **Plain text**: `templates/emails/monthly_summary.txt`

## Testing Locally

To test the command without waiting for the 5th:

```bash
# Edit the command temporarily to remove the date check, OR
# Manually set today to the 5th in a test environment
python manage.py send_monthly_summary
```

To test with specific date:
```python
# In Django shell
from django.utils import timezone
from datetime import date
# Temporarily override timezone.now() in the command for testing
```

## Troubleshooting

### Task not running:
- Check PythonAnywhere task logs
- Verify the command path is correct
- Ensure virtual environment is activated

### Emails not sending:
- Verify Mailgun API key and domain in environment variables
- Check Django error logs: `tail -f /var/log/yourusername.pythonanywhere.com.error.log`
- Test email backend manually:
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'This is a test', 'noreply@paybud.com', ['your@email.com'])
  ```

### Missing users:
- Ensure users have email addresses in their profile
- Users with blank/null email addresses are skipped

## Future Enhancements

- Customize email content (include custom discounts)
- Add weekly summaries option
- Send reports to administrators
- Include charts/graphs in email
- Support for multiple time zones
