import datetime
from datetime import timedelta


def renew_subscription(obj):
    if obj.subscription_end_date:
        obj.subscription_end_date += timedelta(days=30)
    else:
        obj.subscription_end_date = datetime.datetime.now() + timedelta(days=30)
        obj.is_subscribed = True
    return obj.save()
