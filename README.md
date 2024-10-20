Создаем виртуальное окружение: python3 -m venv flask_venv
Активируем venv: source flask_venv/bin/activate
Устанавливаем зависимости: pip install -r requirements.txt
Создаем локальную БД: flask db upgrade
Запуск приложения: flask run

Миграции
Активировать миграции: flask db init
Создать миграцию: flask db migrate -m "comment"
Применить миграции: flask db upgrade