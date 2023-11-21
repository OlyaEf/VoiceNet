from rest_framework import serializers
from datetime import datetime, timedelta
from .models import CDR
import re


class CDRSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов CDR.
    """
    class Meta:
        model = CDR
        fields = '__all__'  # пока, поставила all в проекте поля буду указывать те что не обходимы :-)

    def validate_calling_number(self, value):
        """
        Проверка номера вызывающего абонента.
        """
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):  # Пример регулярного выражения для международного формата номера
            raise serializers.ValidationError("Некорректный формат номера вызывающего абонента.")
        return value

    def validate_called_number(self, value):
        """
        Проверка номера вызываемого абонента.
        """
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError("Некорректный формат номера вызываемого абонента.")
        return value

    def validate(self, data):
        """
        Общая валидация данных CDR.
        """
        # Проверка и преобразование start_time
        if isinstance(data['start_time'], str):
            start_time = datetime.fromisoformat(data['start_time'])
        elif isinstance(data['start_time'], datetime):
            start_time = data['start_time']
        else:
            raise serializers.ValidationError("Неверный формат времени начала.")

        # Проверка и преобразование end_time
        if isinstance(data['end_time'], str):
            end_time = datetime.fromisoformat(data['end_time'])
        elif isinstance(data['end_time'], datetime):
            end_time = data['end_time']
        else:
            raise serializers.ValidationError("Неверный формат времени окончания.")

        # Вычисление продолжительности в секундах
        expected_duration = (end_time - start_time).total_seconds()

        # Получение продолжительности из data['duration'], если это timedelta
        if isinstance(data['duration'], timedelta):
            duration_in_seconds = data['duration'].total_seconds()
        else:
            # Если это строка или число, конвертируем в int
            duration_in_seconds = int(data['duration'])

        # Проверка соответствия продолжительности
        if duration_in_seconds != round(expected_duration):
            raise serializers.ValidationError(
                "Длительность вызова не соответствует времени начала и окончания вызова.")

        return data

    def validate_call_status(self, value):
        """
        Проверка статуса вызова.
        """
        allowed_statuses = [status[0] for status in CDR.CALL_STATUSES]
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                "Некорректный статус вызова. Допустимые значения: {}".format(', '.join(allowed_statuses)))
        return value
