from peewee import SqliteDatabase, Model, CharField

# Підключення до бази даних SQLite
db = SqliteDatabase('settings.db')

# Модель для зберігання налаштувань
class Setting(Model):
    key = CharField(unique=True)
    value = CharField()

    class Meta:
        database = db

# Ініціалізація бази даних
db.connect()

# Створення таблиці
db.create_tables([Setting], safe=True)

# ORM-функції для роботи з налаштуваннями
def save_setting(key, value):
    setting, created = Setting.get_or_create(key=key, defaults={'value': value})
    setting.value = value
    setting.save()

def get_setting(key, default=None):
    try:
        setting = Setting.get(Setting.key == key)
        return setting.value
    except Setting.DoesNotExist:
        return default

def update_setting(key, new_value):
    try:
        setting = Setting.get(Setting.key == key)
        setting.value = new_value
        setting.save()
        return True
    except Setting.DoesNotExist:
        return False

def delete_setting(key):
    try:
        setting = Setting.get(Setting.key == key)
        setting.delete_instance()
        return True
    except Setting.DoesNotExist:
        return False

# Збереження та отримання налаштувань
save_setting('language', 'en')
save_setting('theme', 'dark')

language = get_setting('language', 'en')
theme = get_setting('theme', 'light')

print(f'Language: {language}, Theme: {theme}')

# Оновлення та видалення налаштувань
update_setting('language', 'fr')
deleted = delete_setting('timezone')

# Повторний вивід для перевірки результатів
language = get_setting('language', 'en')
theme = get_setting('theme', 'light')

print(f'Updated Language: {language}, Theme: {theme}')
print(f'Setting "timezone" deleted: {deleted}')

# Закриття з'єднання з базою даних
db.close()
