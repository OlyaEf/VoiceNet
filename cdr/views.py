from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from .cdr_parsers import parse_cdr_csv
from .models import CDR
from .serializers import CDRSerializer


class CDRViewSet(viewsets.ModelViewSet):
    """
        ViewSet для управления записями CDR (Call Detail Records).

        Поддерживаемые операции:
    - Создание новой записи CDR (POST /cdr).
    - Получение списка всех записей CDR (GET /cdr).
    - Получение, обновление или удаление конкретной записи CDR (GET, PUT, DELETE /cdr/:id).
    - Загрузка записей CDR из CSV файла (POST /cdr/upload_cdr).

        Валидация и безопасность:
    - Все запросы к этому ViewSet требуют аутентификации пользователя. Неавторизованные запросы будут отклонены.
    - Поля каждой записи CDR валидируются с использованием CDRSerializer. Это включает проверку формата номеров абонентов, корректности временных меток и длительности звонка.
    - При создании новой записи CDR (POST /cdr) проводится проверка на соответствие всех обязательных полей ожидаемым форматам и ограничениям.
    - При обновлении записи CDR (PUT /cdr/:id) выполняется проверка соответствия изменённых данных требованиям модели.
    - При загрузке данных из CSV файла (POST /cdr/upload_cdr) осуществляется парсинг и валидация каждой строки файла на соответствие формату и правилам модели CDR.
    - Операции, не прошедшие валидацию, отклоняются с сообщениями об ошибках, позволяя пользователю понять и исправить возникшие проблемы.
    - Доступ к операциям управления записями CDR (создание, изменение, удаление) ограничен и требует соответствующих прав доступа.
    """

    queryset = CDR.objects.all()
    serializer_class = CDRSerializer

    def get_queryset(self) -> 'QuerySet[CDR]':
        """
        Возвращает отфильтрованный набор данных в зависимости от параметров запроса.
        Доступные фильтры: start_time, end_time, calling_number, called_number, call_status.
        """
        queryset = CDR.objects.all()
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        calling_number = self.request.query_params.get('calling_number')
        called_number = self.request.query_params.get('called_number')
        call_status = self.request.query_params.get('call_status')

        if start_time and end_time:
            queryset = queryset.filter(start_time__gte=start_time, end_time__lte=end_time)
        if calling_number:
            queryset = queryset.filter(calling_number=calling_number)
        if called_number:
            queryset = queryset.filter(called_number=called_number)
        if call_status:
            queryset = queryset.filter(call_status=call_status)

        return queryset

    @action(detail=False, methods=['post'])
    def upload_cdr(self, request: Request) -> Response:
        """
        Обрабатывает загрузку файла CDR в формате CSV.

        Валидация:
        - Проверяется наличие файла в запросе.
        - Каждая строка файла валидируется и преобразуется в запись CDR.
        """
        cdr_file = request.FILES.get('file')
        if cdr_file:
            parse_cdr_csv(cdr_file)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Файл не предоставлен", status=status.HTTP_400_BAD_REQUEST)
