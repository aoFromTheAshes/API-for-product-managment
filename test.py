import secrets

SECRET = secrets.token_hex(32)  # Генерує 32-байтовий (64 символи) секрет
print(SECRET)
