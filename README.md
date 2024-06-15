# my_currency_service

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone <repository-url>
    cd my_currency_service
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Запуск

1. Запустите FastAPI приложение:
    ```sh
    uvicorn app:app --reload
    ```

2. Приложение будет доступно по адресу `http://127.0.0.1:8000/`

## Тестирование

1. Запустите тесты:
    ```sh
    python -m unittest discover -s tests
    ```
