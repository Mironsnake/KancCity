from django.utils import timezone
from background_task import background

@background(schedule=60)  # Запускаем задачу каждую минуту (для примера, можно установить нужный интервал)
def send_rent_reminder(order_id):
    from django.core.mail import send_mail
    from .models import Order

    order = Order.objects.get(id=order_id)

    # Проверяем, что срок аренды завершается в течение 24 часов
    expiration_time = order.created + timezone.timedelta(days=1)
    if timezone.now() >= expiration_time:
        # Отправляем уведомление пользователю (например, по электронной почте)
        subject = 'Напоминание об окончании срока аренды'
        message = f'Уважаемый {order.user.username}, ваша аренда книги "{order.product.title}" завершается через 24 часа.'
        send_mail(subject, message, 'noreply@example.com', [order.user.email])
