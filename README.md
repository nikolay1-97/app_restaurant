# Описание приложения.
Данное приложение можно представить как REST API сервис для ресторана.
Приложение позволяет выполнять CRUD операции с сущностями "Меню", "Подменю", "Блюда".
Сущность "Подменю" относится к сущности "Меню". Сущность "Блюдо" относится к сущности "Подменю".

При выдаче списка меню, для каждой позиции меню указывается количество связанных с данной позицией позиций подменю.
При выдаче определенной позиции меню, указывается количество связанных с данной позицией позиций подменю и позиций блюд.
При выдаче списка подменю, для каждой позиции подменю указывается количество связанных с данной позицией позиций блюд.
При выдаче определенной позиции подменю, для данной позиции указывается количество связанных с данной позицией позиций блюд.
При удалении позиции меню, так же удаляются все связанные с данной позицией позиции подменю и позиции блюд.
При удалении позиции подменю, так же удаляются все связанные с данной позицией позиции блюд.
В приложении реализовано кэширование запросов с помощью Redis.
Тесты реализованы с помощью Pytest.
## Дополнительные возможности приложения.
В приложении реализована логика управления данными таблиц базы данных из таблицы с расширением .xlsx.
Данная таблица отражает данные таблиц базы данных данного приложения. При изменении данных таблицы .xlsx, данные изменения вносятся в данные таблиц базы данных данного приложения.
Эта функция приложения реализована как фоновая задача с помощью Celery.
Так же, в приложении есть возможность заполнить таблицы базы данных данными из таблицы с расширением .xlsx. Данная таблица(menu.xlsx) находится в корневой директории.
Помимо этого, есть возможность удалить все данные из всех таблиц базы данных.
Приложение можно запустить в Docker. Тесты, так же можно запустить в Docker.
## Техническое описание приложения.
Приложение написано на FastAPI с использованием синтаксиса async/await.
В качестве базы СУБД используется PostgreSQL.
Миграции базы данных реализованы с помощью alembic.
В качестве менеджера зависимостей, в данном приложении используется Poetry.
Тесты написаны на Pytest.
Реализовано кэширование запросов с помощью Redis(инвалидация кэша по времени).
В приложении присутсвует фоновая задача(мониторинг изменений данных приложения из таблицы с расширением .xlsx). Выполняется данная задача с помощью Celery.
В качестве брокера сообщений для Celery, используется RabbitMQ.
Приложение можно запустить в Docker. Тесты, так же можно запустить в Docker.
# Описание структуры приложения.
## Зависимости.
Зависимости находятся в файле "pyproject.toml" в корневой директории.
## Логика управления данными таблиц базы данных.
Логика управления данными таблиц базы данных расположена в "/app/data_sources/storages".
В "/app/data_sources/storage/menu_repository.py" расположен репозиторий для сущности "Меню", в "/app/data_sources/storage/submenu_repository.py" расположен репозиторий
для сущности "Подменю", в "/app/data_sources/storage/dish_repository.py" расположен репозиторий для сущности "Блюда".
## Обработчики запросов.
Обработчики запросов располагаются в /app/views.
В "/app/views/crud_for_menu.py" расположены обработчики запросов для сущности "Меню", в "/app/views/crud_for_submenu.py" расположены обработчики запросов для сущности "Подменю",
в "/app/views/crud_for_dish.py" расположены обработчики запросов для сущности "Блюда".
## Конфигурация приложения.
Конфигурация приложения расположена в "/app/config.py".
Конфигурация для работы тестов, находится в "/tests/conftest.py".
Переменные окружения, необходимые для работы приложения локально, находятся в файле ".env" в корневой директории.
Переменные окружения, необходимые для работы приложения в Docker, находятся в файле ".env-non-dev" в корневой директории.
Переменные окружения, необходимые для работы тестов в Docker, находятся в файле "env-tests" в корневой директории.
## Модели таблиц баз данных.
Модели таблиц базы данных расположены в файле "/app/data_sources/models.py".
## Миграции базы данных.
Миграции базы данных расположены в "/app/migrations/versions".
## Файл запуска приложения.
Приложение запускается из файла "/app/main.py".
## Мониторинг изменения данных таблиц базы данных.
Логика реализации мониторинга изменений данных таблиц базы данных расположена в файле "/app/table_monitoring.py".
## Заполнение таблиц базы данных данными из таблицы с расширением .xlsx.
Логика заполнения таблиц базы данных данными из таблицы с расширением .xlsx расположена в файле "/app/database_entry.py".
## Отчищение таблиц базы данных.
Логика отчищения таблиц базы данных находится в файле "/app/clear_database.py".
## Баш скрипты.
Баш скрипты, необходимы для работы приложения в Docker, расположены в "/scripts_for_docker".
Баш скрипты, необходимы для работы приложения в Docker, расположены в "/scripts_for_docker/app.sh".
Баш скрипты, необходимы для работы тестов в Docker, расположены в "/scripts_for_docker/tests.sh".
# Подготовка к запуску приложения локально.
Для запуска приложения локально, необходимы запущенные сервер PostgreSQL, сервер Redis, сервер RabbitMQ(необходим для работы Celery).
## Подключение к базе данных.
В данном приложении, в качестве СУБД используется PostgreSQL.
Для подключения к базе данных, сначала нужно установить значения для переменных окружения, которые располагаются в файле ".env" в корневой директории.
Необходимо установить значения для следующих переменных:
- DB_USER- имя пользователя базы данных,
- PASSWORD- пароль для базы данных,
- DB_HOST- имя хоста базы данных,
- DB_NAME- имя базы данных,
- DB_PORT- порт базы данных.
После установки данных значений, необходимо выполнить миграцию таблиц базы данных.
Для выполнения миграции таблиц базы данных, необходимо выполнить команду "alembic upgrade head" в терминале из корневой директории.
## Подключение к Redis.
Для подключения к Redis, необходимо установить значения для переменных окружения, которые располагаются в файле ".env" в корневой директории.
Необходимо установить значения для следующих переменных окружения:
- REDIS_HOST- имя хоста Redis,
- REDIS_PORT- порт Redis.
## Установка хоста и порта приложения.
Для работы приложения локально, необходимо установить значения для следующих переменных окружения, которые располагаются в файле ".env" в корневой директории:
- APP_HOST- имя хоста, на котором будет запущено приложение,
- APP_PORT- порт, для запуска приложения.
## Конфигурайия для запуска фоновой задачи и заполнения базы данных из таблицы с расширением .xlsx.
Для запуска фоновой задачи(мониторинг изменения данных таблиц базы данных), необходиомо указать URL брокера сообщений.
Так же, для запуска фоновой задачи, нужно указать абсолютный путь до таблицы с расширением .xlsx, изменения данных которой,
будут влиять на изменение данных таблиц базы данных. Путь до данной таблицы .xlsx, так же необходим для реализации заполнения
таблиц базы данных, данными из этой таблицы.
Так же для выполнения фоновой задачи, необходимо укзать частоту проверки состояния таблицы .xlsx.
В общем, нужно установить значения для следующих переменных окружения, которые распологаются в файле ".env" в корневой директории:
- PATH_TO_TABLE- абсолютный путь до таблицы с расширением .xlsx,
- BROKER_URL- URL брокера сообщений(RabbitMQ),
- CHECK_INTERVAL- частота проверки состояния таблицы .xlsx.
