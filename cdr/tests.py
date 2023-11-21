import os

from django.test import TestCase
from .serializers import CDRSerializer
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth.models import User


class CDRSerializerTestCase(TestCase):
    """ Тестирование сериализатора CDR."""
    def test_valid_serializer(self) -> None:
        """Тест валидного сериализатора."""
        valid_data = {
            'call_id': '12345678',
            'calling_number': '+11234567890',
            'called_number': '+10987654321',
            'start_time': '2023-11-20T22:00:00Z',
            'end_time': '2023-11-20T22:10:00Z',
            'duration': '600',
            'call_status': 'SUCCESS',
            'call_type': 'OUTGOING'
        }
        serializer = CDRSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self) -> None:
        """Тест невалидного сериализатора."""
        invalid_data = {
            'call_id': '',
            # другие поля
        }
        serializer = CDRSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class CDRViewSetTestCase(APITestCase):
    """Тестирование API для CDR."""
    def setUp(self) -> None:
        # Создание суперпользователя в тестовой базе данных
        self.superuser = User.objects.create_superuser(
            username='test@gmail.com',
            email='test@gmail.com',
            password='Test@12345678'
        )
        self.client = APIClient()
        response = self.client.post('/api/token/', {
            'username': 'test@gmail.com',
            'password': 'Test@12345678'
        })

        print(response.data)  # Для отладки

        self.token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_list_cdr(self):
        """Тест запроса списка CDR."""
        response = self.client.get('/cdr/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cdr(self):
        """Тест создания записи CDR."""
        data = {

            "call_id": "12345678",
            "calling_number": "+11234567891",
            "called_number": "+10987654321",
            "start_time": "2023-11-20T22:00:00Z",
            "end_time": "2023-11-20T22:10:00Z",
            "duration": "600",
            "call_status": "SUCCESS",
            "call_type": "OUTGOING"
}
        response = self.client.post('/cdr/', data)
        print(response.data)  # строка для отладки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_cdr_by_start_time(self):
        """Тест фильтрации CDR по времени начала."""
        response = self.client.get('/cdr/?start_time=2023-11-20T22:00:00Z')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
