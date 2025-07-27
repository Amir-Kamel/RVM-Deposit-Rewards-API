from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum

def send_deposit_summary_email(user, total_weight, total_reward_points, total_used_points, remaining_points):
    subject = "🧾 Your Drop Me Recycling Summary"
    message = (
        f"Hello {user.username},\n\n"
        f"Thank you for using Drop Me's smart recycling system! ♻️\n\n"
        f"Here’s your current recycling summary:\n"
        f"➤ Total Weight Deposited: {total_weight:.2f} kg\n"
        f"➤ Total Reward Points Earned: {total_reward_points} points\n"
        f"➤ Total Points Used: {total_used_points} points\n"
        f"➤ Remaining Points Available: {remaining_points} points\n\n"
        f"Keep recycling and earning rewards with Drop Me!\n\n"
        f"Best regards,\n"
        f"The Drop Me Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


