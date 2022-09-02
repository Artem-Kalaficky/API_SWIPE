import datetime

from celery import shared_task

from users.services.subscription_renewal import renew_subscription


@shared_task
def check_subscription_status():
    from .models import UserProfile

    users = UserProfile.objects.filter(is_staff=False, is_developer=False, is_subscribed=True)
    for user in users:
        if user.subscription_end_date:
            if user.subscription_end_date < datetime.datetime.now().date():
                if user.is_auto_renewal:
                    renew_subscription(user)
                    print('Подписка автоматически продлена!')
                else:
                    user.subscription_end_date = None
                    user.is_subscribed = False
                    user.is_auto_renewal = False
                    user.save()
                    print('Подписка снята!')
            print('Подписка ещё активна')
