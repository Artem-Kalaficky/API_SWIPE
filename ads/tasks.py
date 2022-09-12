import datetime

from celery import shared_task


@shared_task
def check_promotion_status():
    from ads.models import Promotion

    promotions = Promotion.objects.all()
    for promotion in promotions:
        if promotion.end_date < datetime.datetime.now().date():
            promotion.delete()
            print('Удалено')
        else:
            print('Продвижения в порядке')
