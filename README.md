# url-shortener
Учебный проект в рамках курса "Прикладной Python" в ВШЭ

Требования: https://colab.research.google.com/drive/1_XpbChwNfdSu0k2cBItKDfAX3YOWxU3S?usp=sharing


**API:**

1. POST /api/v1/links/shorten
   
Создание новой короткой ссылки

request body:
{
  "full_url": "string", # оригинальный url 
  
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", # id пользователя, соверщающего запрос
  
  "expires_at": "2025-03-31T18:01:22.927Z", # дата, с которой ссылка перестает быть актуальной, может быть null
  
  "custom_alias": "string" # короткая ссылка, может быть null
}

Пример запроса:
curl -X 'POST' \
  'http://localhost:8080/api/v1/links/shorten' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "full_url": "https://www.hse.ru/",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "expires_at": "2025-03-31T18:08:57.165Z",
  "custom_alias": "hse"
}'


2. GET /api/v1/links/search

Получение ссылок по фильтрам

query params:

ids: array<any> # список системных id, присваемых ссылкам 

short_url: string # короткая ссылка

origin_url: string # оригинальный url 


Пример запроса:
curl -X 'GET' \
  'http://localhost:8080/api/v1/links/search' \
  -H 'accept: application/json'

3. GET /api/v1/links/{short_url}

Редирект пользователя по короткой ссылке

path variable:

short_url: string # короткая ссылка


Пример запроса:
curl -X 'GET' \
  'http://localhost:8080/api/v1/links/hse' \
  -H 'accept: application/json'

4. DELETE /api/v1/links/{short_url}
   
Удаление короткой ссылки

path variable:

short_url: string # короткая ссылка


Пример запроса:
curl -X 'DELETE' \
  'http://localhost:8080/api/v1/links/hse' \
  -H 'accept: application/json'

5. PUT /api/v1/links/{short_url}
   
Обновление короткой ссылки

path variable:

short_url: string # текущая короткая ссылка


query params:

new_short_url # новая короткая ссылка


Пример запроса:
curl -X 'PUT' \
  'http://localhost:8080/api/v1/links/hse?new_short_url=msu' \
  -H 'accept: application/json'

6. GET /api/v1/links/{short_url}/stats
   
Получение статистики по ссылке

path variable:

short_url: string # короткая ссылка


Пример запроса:
curl -X 'GET' \
  'http://localhost:8080/api/v1/links/hse/stats' \
  -H 'accept: application/json'


**Инструкцию по запуску:**

1. Установить Git, Docker
   
3. Выполнить git pull https://github.com/diefrein/url-shortener.git
   
5. Выполнить docker compose up -d
   

**Описание БД:**

1. Таблица urls
   
urls

(

    id uuid primary key default gen_random_uuid(), 
    
    full_url varchar not null, 
    
    short_url varchar not null, 
    
    user_id uuid not null
    
)


3. unique index on urls(short_url)
   

5. Таблица users (пока не используется)
   
users

(

    id uuid primary key default gen_random_uuid(), 
    
    name varchar not null
    
)
