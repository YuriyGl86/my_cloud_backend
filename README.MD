# Облачное хранилище MyCloud
## Основные моменты.
1. #### Проект разделен на два репозитория:

   * Frontend : [GitHub Frontend](https://github.com/YuriyGl86/my_cloud_frontend)
   * Backend: [GitHub Backend](https://github.com/YuriyGl86/my_cloud_backend)

    При этом, backend-репозиторий содержит самодостаточный, полностью работоспособный код, готовый для развертывания 
(включает в себя bild от frontend-части). Код во frontend репозитории так же полностью работоспособный, но требует 
отдельно запущенного backend-сервера для работы с api-запросами. 

2. #### Frontend.

    Т.к. в задании указано, что 'не предполагает существенных усилий по оформлению приложения' и 
'не боимся самостоятельно принимать решения по проекту', то:
    * почти весь UI дизайн построен на элементах из внешней библиотеки ANT Design.
    * всё что касается взаимодействия с API реализовано через RTK Query

3. #### Backend.
    По тем же причинам, в backend части приложения решено:
   * Использовать авторизацию по токенам, т.к. для облачного хранилища SessionBase авторизация неудобна, 
а авторизация по JWT избыточная для требуемого функционала.
   * Для авторизации использовать сторонний пакет Djoser с небольшими изменениями для соответствия требованиям задания,
т.к. именно так рекомендует делать документация DRF для реализации TokenAuthentication.
   * Использовать встроенную таблицу User, т.к. она полностью покрывает требования и содержит требуемые поля.


## Развертывание приложения на сервере.
1. Через любого хостинг-провайдера создать сервер под управлением Ubuntu. 
    * Версия 20.04 или выше
    * Для подключения удобно использовать SSH-ключ. Для этого предварительно нужно создать пару из публичного и приватного ключа у себя на компьтере через консоль командой `ssh-keygen`, после чего в файле *~/.ssh/id_rsa.pub* скопировать публичный ключ. Далее при создании серера добавить этот SSH-ключ (можно сделать это позднее через личный кабинет или непосредственно на сервере).
2. Подключиться к серверу и создать пользователся с правами суперпользователя через которого будет настраиваться и работать сервер  (т.к. у пользователя root слишком большие полномочия). Авторизуйемся от его имени.
    * ***ssh root@89.111.171.38*** - логин root и IP предоставляет хостинг-провайдер после создания сервера
    * **adduser yuriy** - здесь и далее в качестве примера будет использоваться пользователь yuriy.
    * ***usermod yuriy -aG sudo*** - добавляем созданного пользователя в группу суперпользователей.
    * ***logout***
    * ***ssh yuriy@89.11.171.38***  - заходим от имени созданного пользователя.
3. Устанавливаем нужную версию python. Для данного приложения нужна версия 3.11.7:
    * ***python3 --version***  - проверяем что установлено сейчас, если установлено. Если не 3.11, то продолжаем следующие шаги.
    * ***sudo add-apt-repository ppa:deadsnakes/ppa*** - добавляем репозиторий с прошлыми версиями python.
    * ***sudo apt install --reinstall software-properties-common***  - ЕСЛИ ПРЕДЫДУЩИЙ ШАГ ЗАКОНЧИЛСЯ ОШИБКОЙ, например, если сначала были обновлены репозитории через sudo apt update, то тогда поможет эта команда.
    * ***sudo apt-get update***  - обновляем спсиок репозиториев.
    * ***sudo apt-get install python3.11*** - устанавливаем нужную версию python, в данном случае 3.11.
4. Обновляем список репозиториев пакетного менеджера и обновляем все до последних версий.
    * ***sudo apt update***
    * ***sudo apt upgrade*** - не обязательно, но желательно.
5. Устанавливаем нужные пакеты, по отдельности или одной командой.
    * ***sudo apt install python3.11-venv python3-pip postgresql nginx*** - устанавливаем виртуальное окружение для установленной версии python (3.11 в нашем случае), пакетный менеджер pip, postgresql и веб-сервер nginx.
6. Создаем пользователя для работы с postgresql (не обязательно, можно использовать и пользователя postgres) и создаем базу данных для приложения.
    * ***sudo systemctl status postgresql*** - проверяем что postgres запустился и работает
    * ***sudo su postgres***  - переключаемся на пользователя postgres
    * ***psql*** - заходим в psql
    * ***CREATE USER yuriy WITH SUPERUSER;*** - создаем пользователя yuriy
    * ***ALTER USER yuriy WITH PASSWORD '1234';*** - назанчаем пароль
    * ***CREATE DATABASE yuriy;*** - создаем пустую базу. Она не будет использоваться далее, но это необходимый шаг, без этого работать не будет.
    * ***\q***  - выходим из psql
    * ***exit***  - разлогиниваемся от пользователя postgres
    * ***psql***  - заходим снова, но уже используя учетный данные созданного пользователя yuriy
    * ***CREATE DATABASE my_cloud;*** - создаем базу данных для нашего приложения. 
    * ***\q*** - выходим из psql
7. Клонируем репозиторий с проектом на сервер.
    * ***git --version***  - проверяем что git установлен.
    * ***git clone https://github.com/YuriyGl86/my_cloud_backend.git*** - клонируем репозиторий.
    * ***git checkout {name}*** - если надо, переходим в нужную ветку репозитория (в нашем случае не надо)
8. Настраиваем переменные окружения.
    * ***nano .env***  - открываем файл с переменными в корне проекта и если что-то изменилось, то вносим необходимые правки.
9. Создаем, активируем виртуальное окружение для проекта. Устанавливаем зависимости.
    * ***python3.11 -m venv venv*** - находясь в папке проекта, создаем окружение с нужным именем, например venv
    * ***source venv/bin/activate*** - активируем созданное виртуальное окружение
    * ***pip install -r requirements.txt*** - устанавливаем зависимости.
    * ***pip freeze*** - проверяем список установленных пакетов, если чего-то не хватает, доустанавливаем.
    * ***pip install gunicorn*** - если не установлен gunicorn (в нашем случае, должен установиться сам из requirements)
    * ***python manage.py migrate*** - применяем миграции.
    * ***python manage.py createsuperuser*** - создаем суперпользователя (можно и без этого, регистрироваться через само приложение, но тогда будет невозможно создать хотя бы одного пользователя с правами администратора).
    * ***python manage.py collectstatic*** - собираем все статические файлы проекта в одну папку, указанную через переменную окружения в файле .env.
10. Проверяем, что на данном этапе всё работает.
    * ***python manage.py runserver 0.0.0.0:8000*** - запускаем отдельно django-приложение. Пробуем зайти через браузер по IP адресу сервера, указав порт.
    * ***fuser -k 8000/tcp*** - если порт занят после нештатного завершения предыдущего процесса, то эта команда убъет процесс и освободит порт.
    * ***gunicorn my_cloud.wsgi -b 0.0.0.0:8000*** - пробуем подключиться через gunicorn, указываем путь к файлу wsgi, в данном случае файл wsgi.py  лежит в папке проекта my_cloud, указываем интерфейс для отслеживания - 0.0.0.0:8000. Пробуем зайти через браузер по IP адресу сервера, указав порт.
11. Настраиваем gunicorn. Делаем  gunicorn сервисом в нашей системе, т.е. был постоянно запущен и при старте системы автоматически запускался сам.
    * ***sudo nano /etc/systemd/system/gunicorn.service*** - создаем файл настроек gunicorn-сервиса. Внутри указываем следующие настройки:
        ```
        [Unit]	
        Description=gunicorn service	
        After=network.target	
        [Service]	
        User=yuriy	
        Group=www-data	
        WorkingDirectory=/home/yuriy/my_cloud_backend/my_cloud	
        ExecStart=/home/yuriy/my_cloud_backend/venv/bin/gunicorn --access-logfile -\	
        --workers=1 \	
        --bind unix:/home/yuriy/my_cloud_backend/my_cloud/my_cloud/project.sock my_cloud.wsgi:application	
        [Install]	
        WantedBy=multi-user.target
        ```
        + В разделе `[unit]`, в котором указываются мета-данные и зависимости, прописываем описание создаваемого сервиса: `Description=gunicorn service` и `After=network.target` - указываем когда должен запускаться сервис, в нашем случае т.к. нам нужно подключение к сети, то указываем запуск после запуска сетевых служб.
        + В разделе `[Service]` указываем пользователя `User=yuriy` и группу `Group=www-data`. Это группа нашего nginx, он ее создает сам. Далее в переменной `WorkingDirectory` указываем рабочую папку проекта, в которой находится файл manage.py. Далее, в переменно `ExecStart`  указываем какой командой создаваемый сервис gunicorn запускать. В этой команде --access-logfile - значит что аксес-лог файл не нужен, указано число воркеров (число ядер *2), и в bind указываем какой интерфейс нужно отслеживать -  путь к папке где лежит файл wsgi, в этой папке создастся файл project.sock, который будет точкой подключения nginx к gunicorn; указываем что в файле wsgi есть переменная application и нужно обращаться к ней.
    * ***sudo systemctl start gunicorn*** - запускаем сервис, и если все сделано правильно, то не должно быть ошибок
    * ***sudo systemctl enable gunicorn*** - включаем сервис
    * ***sudo systemctl status gunicorn*** - проверяем статус
12. Настраиваем веб-сервер nginx, чтобы он мог подключаться к gunicorn через сокет project.sock и уже через него передавать дальше запрос к django приложению.
    * ***sudo nano /etc/nginx/sites-available/my_cloud*** - создаем файл настроек.
    * в созданном файле указываем следующие дерективы:
        ```
        server {
            listen 80;
            server_name 89.111.155.64;
            access_log  /var/log/nginx/guni-access.log;
            error_log  /var/log/nginx/guni-error.log info;

            location /static/ {
                    root home/yuriy/my_cloud_backend/my_cloud;
            }
            location / {
                    include proxy_params;
                    proxy_pass http://unix:/home/yuriy/my_cloud_backend/my_cloud/my_cloud/project.sock;
            }
        }
        ```
        здесь:
        + деректива `listen` - указывает, какой порт слушать серверу, по умолчанию 80.
        + `server_name` - доменное имя сервера, т.к. его у нас нет, то указываем IP
        + `access_log` и `error_log` - указываем куда будут писаться логи с запросами и с ошибками.
        + `location /static/` если пользователь в пути обращается к static, то указываем где искать статику
        + `location /` - как обрабаывать все остальные пути
            - `include proxy_params` - указываем что нужно проксировать запросы
            - `proxy_pass http://unix:/home/yuriy/my_cloud_backend/my_cloud/my_cloud/project.sock` - указываем коуда обращаться nginx чтобы передать запрос в django - путь до файла сокета.
    * ***sudo nginx -t*** - проверяем что в файле настрроек нет ошибок
    * ***sudo ln -s /etc/nginx/sites-available/my_cloud /etc/nginx/sites-enabled*** - чтобы "включить" сайт, делаем символическую ссылку, "переносим" из avalible в enabled
    * ***sudo ufw allow 'Nginx Full'*** - настройка firewall, разрешаем полные права Nginx для подключения
    * ***sudo systemctl reload nginx*** - перезагруаем сервер nginx
    * ***sudo systemctl status nginx*** - проверяем статус
    * ***sudo nano /etc/nginx/nginx.conf*** - заходим в файл настроек nginx:
        + В секции http указываем допустимый размер тела запроса: 
            ```
            http {
                client_max_body_size 20M;         
            }
            ```
        + Если возникает ошибка 502, то:
            ```
                user yuriy www-data;
            ```
            в первой же строчке указываем юзера как yuriy и группу www-data которую сам nginx делает
