# Установка и запуск проекта (локально, без Docker)

Данная инструкция поможет вам развернуть проект Django на вашем компьютере для разработки.

## Требования

- **Python 3.12 или новее** (рекомендуется 3.12)
- **PostgreSQL 16** (или 15, 14)
- **Git**
- Операционная система: Linux (Ubuntu/Debian), Windows (WSL2 рекомендуется) или macOS

## 1. Установка PostgreSQL

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install postgresql-16 postgresql-contrib-16
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Windows

Скачайте установщик с официального сайта (https://www.postgresql.org/download/windows/) и установите PostgreSQL 16.
В процессе запомните пароль суперпользователя postgres.

### macOS

```bash
brew install postgresql@16
brew services start postgresql@16
```

## 2. Создание базы данных и пользователя

Подключитесь к PostgreSQL и выполните команды (замените ваш_пароль на надежный пароль):
```bash
sudo -u postgres psql
```

Внутри psql:
```sql
CREATE USER django_user WITH PASSWORD 'ваш_пароль';
CREATE DATABASE django_accounting OWNER django_user;
GRANT ALL PRIVILEGES ON DATABASE django_accounting TO django_user;
\q
```

Проверьте, что база создалась:
```bash
sudo -u postgres psql -l | grep django_accounting
```

Или установите DBVeawer, pgAdmin, HeidiSQL или любое другое приложение для работы с базами данных, которое поддерживает PostGreSQL.

### 3. Клонирование репозитория

```bash
git clone https://github.com/HighLander26rus/django-accounting.git
cd django-accounting
```

### 4. Создание виртуального окружения и установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# или для Windows: venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл .env в корне проекта (там же, где manage.py):
```bash
nano .env   # или используйте любой редактор
```

Содержимое .env:
```ini
DB_NAME=django_accounting
DB_USER=django_user
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

**Важно:** Никогда не загружайте .env в Git (он уже в .gitignore).

### 6. Применение миграций

```bash
python manage.py migrate
```

Вы должны увидеть сообщения о применении миграций.

### 7. Загрузка тестовых данных

```bash
python manage.py shell < load_test_data.py
```

Или:
```bash
python manage.py runscript load_test_data   # если установлен django-extensions
```

Вручную (если не работает):
```bash
python manage.py shell
>>> exec(open('load_test_data.py').read())
```

Убедитесь, что в консоли появились сообщения о создании клиентов, товаров и т.д.

### 8. Создание суперпользователя для входа в админку

```bash
python manage.py createsuperuser
```

Введите логин (например, admin), email (можно пропустить), пароль.

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере: http://127.0.0.1:8000/admin/

Войдите под суперпользователем. Вы должны увидеть админ-панель со всеми моделями (Клиенты, Товары, Партии, Транзакции и т.д.)

### 10. Проверка работы сервисных функций (по желанию)

Запустите shell и выполните тестовый сценарий:
```bash
python manage.py shell
```

Вставьте код из тестового скрипта (пример в основном README).

### 11. Возможные проблемы и их решение
**Ошибка: psycopg2 не устанавливается**

Установите системные зависимости:

```bash
sudo apt install libpq-dev python3-dev   # Debian/Ubuntu
```

**Ошибка: role "django_user" does not exist**

Проверьте, что вы создали пользователя в PostgreSQL и правильно указали имя в .env.

**Ошибка: could not translate host name "db" to address**

Убедитесь, что в .env указан DB_HOST=localhost, а не db.

**Ошибка при загрузке тестовых данных**

Убедитесь, что миграции выполнены, и вы находитесь в корневой папке проекта (там, где manage.py).

### 12. Готово!

Теперь вы можете приступать к выполнению заданий из папки tasks/.
