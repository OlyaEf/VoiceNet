import csv
from datetime import datetime
from .serializers import CDRSerializer


def parse_cdr_csv(file):
    """
   Функция для парсинга и обработки данных CDR из CSV файла.
   """
    reader = csv.reader(file)
    next(reader, None)  # Пропуск заголовка, если он есть
    for row in reader:
        try:
            cdr_data = {
                'call_id': row[0],
                'calling_number': row[1],
                'called_number': row[2],
                'start_time': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                'end_time': datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
                'duration': int(row[5]),  # Преобразование в целое число, если продолжительность указана в секундах
                'call_status': row[6],
                'call_type': row[7]
            }
            serializer = CDRSerializer(data=cdr_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except ValueError as e:
            print(f"Ошибка обработки данных: {e}")
