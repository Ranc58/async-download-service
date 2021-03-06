# Микросервис для скачивания файлов

Микросервис помогает работе основного сайта, сделанного на CMS и обслуживает
запросы на скачивание архивов с файлами. Микросервис не умеет ничего, кроме упаковки файлов
в архив. Закачиваются файлы на сервер через FTP или админку CMS.

Создание архива происходит на лету по запросу от пользователя. Архив не сохраняется на диске, вместо этого по мере упаковки он сразу отправляется пользователю на скачивание.

От неавторизованного доступа архив защищен хешом в адресе ссылки на скачивание, например: `http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/`. Хеш задается названием каталога с файлами, выглядит структура каталога так:

```
- photos
    - 3bea29ccabbbf64bdebcc055319c5745
      - 1.jpg
      - 2.jpg
      - 3.jpg
    - af1ad8c76fda2e48ea9aed2937e972ea
      - 1.jpg
      - 2.jpg
```
## Как запустить с помощью Docker

1) `cp env/.env env/.env_file`
2) задайте настройки в `env/.env_file`: 
   - `LOGGING=1` если необходимо логгирование.
   - `RESPONSE_TIMEOUT` при  необходимости увеличения времени ответа (по умолчанию 0.01)
   - `HOST` и `PORT`. по умолчанию стоит `0.0.0.0` и `8080` порт.
   
   По умолчанию фотографии беруться из директории `test_photos` в корне проекта.
   Если необходимо поменять - измените в `docker-compose.yml` в разделе `volumes` `- ./test_photos:/app/photos` 
   на `- <ПОЛНЫЙ ПУТЬ ДО ВАШИХ ФОТО>:/app/photos`.
3) Для локальной разработки можно  использовать `docker-compose -f docker-compose.dev.yml build` и потом использовать `docker-compose -f docker-compose.dev.yml up` (Папка с приложением будет примонтирована и можно не собирать каждый раз заново образ.). В остальных случаях `docker-compose up --build`
## Как установить

Для работы микросервиса нужен Python версии не ниже 3.6.

```bash
pip install -r app/requirements.txt
```

## Как запустить
1) По умолчанию сервис рабоатет на локальном хосте, порте 8080, с отклюбченным логгированием, используя директорию `./test_photos` для фото.
 При необходимости смены каких либо параметров `cp env/.env env/.env_file` и задать настройки в `env/.env_file`:
   - `LOGGING=1` если необходимо логгирование.
   - `RESPONSE_TIMEOUT` при  необходимости увеличения времени ответа (по умолчанию 0.01)
   - `HOST` и `PORT`.
   - `PHOTOS_PATH` для указания новой папки с фото (поддерживается только полный путь!)
2) Запуск: `python app/server.py`


Сервер запустится на порту 8080, чтобы проверить его работу перейдите в браузере на страницу [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Как развернуть на сервере

1) По умолчанию сервис рабоатет на локальном хосте, порте 8080, с отклюбченным логгированием, используя директорию `./test_photos` для фото.
 При необходимости смены каких либо параметров `cp env/.env env/.env_file` и задать настройки в `env/.env_file`:
   - `LOGGING=1` если необходимо логгирование.
   - `RESPONSE_TIMEOUT` при  необходимости увеличения времени ответа (по умолчанию 0.01)
   - `HOST` и `PORT`.
   - `PHOTOS_PATH` для указания новой папки с фото (поддерживается только полный путь!)
2) Запуск: `python app/server.py`

После этого перенаправить на микросервис запросы, начинающиеся с `/arhive/`. Например:

```
GET http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/
GET http://host.ru/archive/af1ad8c76fda2e48ea9aed2937e972ea/
```

# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
