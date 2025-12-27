Веб-приложение для управления автомойкой с онлайн-бронированием.

Возможности
- Онлайн-бронирование: Клиенты могут записываться на услуги онлайн
- Управление услугами: Каталог услуг с категориями и ценами
- Система скидок: Накопительные скидки для постоянных клиентов
- Профили клиентов: Личные кабинеты с историей записей
- Управление персоналом: Учет сотрудников и их расписания
- Административная панель: Полный контроль через Django Admin

Технологии
- Backend: Django 3.2.16, Python 3.10+
- Frontend: Bootstrap 5, Django Templates
- База данных: SQLite (для разработки)
- Тестирование: pytest, Django Test Framework


```bash
# Клонирование
git clone https://github.com/Svetlanausacheva/carwash-project.git
cd carwash-project

# Виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Зависимости
pip install -r requirements.txt

# База данных
python manage.py migrate
python manage.py createsuperuser

# Запуск
python manage.py runserver
