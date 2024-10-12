import os
from config.config import TEST_DB_PATH

# Функция для удаления тестовой базы данных
def remove_test_db():
    db_path = TEST_DB_PATH
    if os.path.exists(db_path):
        os.remove(db_path)
