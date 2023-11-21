from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import CdrConfig
from .views import CDRViewSet


app_name = CdrConfig.name


# Создание роутера и регистрация нашего ViewSet
router = DefaultRouter()
router.register(r'cdr', CDRViewSet)

# URL-паттерны API теперь автоматически определены роутером.
urlpatterns = [
    path('', include(router.urls)),

] + router.urls
