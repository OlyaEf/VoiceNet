from django.db import models
from typing import List, Tuple
from django.utils.translation import gettext_lazy as _


class CDR(models.Model):
    """
    Модель для хранения информации о звонках (Call Detail Record - CDR).

    Атрибуты:
    - call_id: Уникальный идентификатор вызова.
    - calling_number: Номер телефона вызывающего абонента.
    - called_number: Номер телефона вызываемого абонента.
    - start_time: Время начала звонка.
    - end_time: Время окончания звонка.
    - duration: Продолжительность звонка.
    - call_status: Статус звонка (например, успешный, неотвеченный).
    - call_type: Тип звонка (например, исходящий, входящий).
    """
    CALL_STATUSES: List[Tuple[str, str]] = [
        ('SUCCESS', 'Успешный'),
        ('UNANSWERED', 'Неотвеченный'),
        ('REJECTED', 'Отклоненный'),
    ]

    CALL_TYPES: List[Tuple[str, str]] = [
        ('OUTGOING', 'Исходящий'),
        ('INCOMING', 'Входящий'),
        ('MISSED', 'Пропущенный'),
    ]

    call_id = models.CharField(max_length=100, verbose_name=_('Call ID'))
    calling_number = models.CharField(max_length=20, verbose_name=_('Calling Number'))
    called_number = models.CharField(max_length=20, verbose_name=_('Called Number'))
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    duration = models.DurationField(verbose_name=_('Duration'))
    call_status = models.CharField(max_length=50, choices=CALL_STATUSES, verbose_name=_('Call Status'))
    call_type = models.CharField(max_length=50, choices=CALL_TYPES, verbose_name=_('Call Type'))

    def __str__(self):
        return f"CDR Record for {self.calling_number} to {self.called_number} at {self.start_time}"
