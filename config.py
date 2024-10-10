from dotenv import load_dotenv
import os

# Завантаження змінних оточення з файлу .env
load_dotenv(dotenv_path="C:/Users/vchep/Desktop/SEXY_codes/FastApi/docuapp/.env")
# Отримання змінних з оточення
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Друкування для перевірки, що змінні завантажуються
print(f"DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}, DB_PASS: {DB_PASS}")

# Перевірка наявності необхідних змінних
assert DB_HOST, "DB_HOST is not set"
assert DB_PORT, "DB_PORT is not set"
assert DB_NAME, "DB_NAME is not set"
assert DB_USER, "DB_USER is not set"
assert DB_PASS, "DB_PASS is not set"


