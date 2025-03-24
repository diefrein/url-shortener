import hashlib
import string
import random

def generate_short_url(full_url: str, length: int=6):
    # Создаем хеш от длинной ссылки (SHA256)
    hash_object = hashlib.sha256(full_url.encode())
    hex_dig = hash_object.hexdigest()
    
    # Преобразуем часть хеша в целое число
    num = int(hex_dig[:8], 16)
    
    # Символы для base62 (0-9, A-Z, a-z)
    characters = string.digits + string.ascii_letters
    base62 = []
    
    # Конвертируем число в base62
    for _ in range(length):
        num, rem = divmod(num, 62)
        base62.append(characters[rem])
    
    # Перемешиваем для большей случайности
    random.shuffle(base62)
    return ''.join(base62)[:length]