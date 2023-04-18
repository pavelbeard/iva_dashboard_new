<h1 style="text-align: center">Приложение IVA MCU Dashboard</h1>

<p style="text-align: center">
Created by pavelbeard
<br>v0.6.94</p>

Введение:
  <ul>
    <li><a href="#about">Краткое описание</a></li>
    <li><a href="#howToInstall">Как установить?</a></li>
    <li>Как пользоваться?</li>
  </ul>

<div id="about">
<h2>1. Краткое описание</h2>
    Сей веб-сервис используется для мониторинга системы ВКС IVA MCU.<br> 
    <div style="text-align: center">Главная страница выглядит так:</div><br><br>
    <img src="doc_pics/img.png" alt="main"><br><br>
    На ней изображен мониторинг серверов IVA. На каждом сервере мониторятся:
    <ul>
        <li>Процессор</li>
        <li>ОЗУ</li>
        <li>Диски(виртуальные) и файловые системы</li>
        <li>Состояние потоков приложений и служб</li>
        <li>Состояние приложений и служб</li>
        <li>Состояние сетевых интерфейсов</li>
        <li>Мероприятия</li>
    </ul>
    В правой части панели отображен мониторинг журнала событий
    и возраст TLS сертификата 
    <br>
    <br>
    В будущем ожидается:
    <ul>
        <li>графики</li>
        <li>панель мероприятий</li>
        <li>панель лицензий</li>
        <li>панель пользователей IVA</li>
    </ul>
</div>
<div id="howToInstall">
<h2>2. Как установить?</h2>

<div>
<ul>
    <li>Скачиваем репозиторий</li>
    <pre>
    wget https://github.com/pavelbeard/iva_dashboard_new
    </pre>
    <li>Заходим в папку iva_dashboard_new</li>
    <pre>
    cd iva_dashboard_new
    </pre>
    <li>Меняем переменные окружения в файлах в папке /env и <br>
    /monitor_serv_frontend/nginx:
        <ul>
            <li>файл prod.monitor-postgres.env содержит:
                <ul>
                    <li><b>POSTGRES_USER=имя админа базы данных</b></li>
                    <li><b>POSTGRES_PASSWORD=пароль БД</b></li>
                    <li><b>POSTGRES_DB=имя базы данных</b></li>
                </ul>
            </li>
            <li>файл prod.monitor-serv.env содержит
                <ul>
                    <li><b>SECRET_KEY=секретный ключ приложения, для API</b></li>
                    <li><b>DEBUG=режим отладки. в продакшн должен быть отключен</b></li>
                    <li><b>ENGINE=движок баз данных</b></li>
                    <li><b>POSTGRES_DB_HOST=хост базы данных приложения</b></li>
                    <li><b>POSTGRES_DB_PORT=порт</b></li>
                    <li><b>POSTGRES_DB_USER=пользователь</b></li>
                    <li><b>POSTGRES_DB_PASSWORD=пароль</b></li>
                    <li><b>POSTGRES_DB_NAME=имя бд</b></li>
                    <li><b>IVCS_POSTGRES_DB_NAME=имя базы данных IVA</b></li>
                    <li><b>IVCS_POSTGRES_DB_USER=пользователь</b></li>
                    <li><b>IVCS_POSTGRES_DB_PASSWORD=пароль</b></li>
                    <li><b>IVCS_POSTGRES_DB_HOST=хост</b></li>
                    <li><b>IVCS_POSTGRES_DB_PORT=порт</b></li>
                    <li><b>SCHEMAS=если есть схемы в базе данных - ставим</b></li>
                    <li><b>CSRF_TRUSTED_ORIGINS=домены, с которых могут поступать запросы 
                    от аутентифицированных пользователей</b></li>
                    <li><b>DJANGO_SUPERUSER_USERNAME=имя админа приложения</b></li>
                    <li><b>DJANGO_SUPERUSER_EMAIL=email админа</b></li>
                    <li><b>DJANGO_SUPERUSER_PASSWORD=пароль по умолчанию</b></li>
                    <li><b>MONITOR_SERVER_ADDRESS=адрес сервера</b></li>
                    <li><b>MONITOR_SERVER_PORT=порт сервера</b></li>
                </ul>
            </li>
            <li>файл prod.monitor-serv-frontend содержит:
                <ul>
                    <li><b>REACT_APP_BACKEND_URL=адрес API-сервера</b></li>
                    <li><b>REACT_APP_IVCS_API_URL=скоро будет удалена</b></li>
                    <li><b>REACT_APP_DEBUG=режим отладки. в продакшн должен быть отключен</b></li>
                    <li><b>REACT_APP_MAIL_TO_DEV=email администратора</b></li>
                    <li><b>REACT_APP_CALL_TO_DEV=телефон администратора</b></li>
                    <li><b>NODE_ENV=должно стоять production</b></li>
                </ul>
            </li>
        </ul>
    </li>
    <li>Запускаем команду сборки docker-compose</li>
    <pre>
    docker-compose -f prod.docker-compose.yml up -d --build
</pre>
</ul>
</div> 
<div id="howToUse">
<h2>3. Как использовать?</h2>
<ul>
    <li>Регистрируемся в системе
    <br>
    <img src="doc_pics/register.png" alt="register">
    </li>
    <li>
    Ожидаем активации вашего аккаунта администратором
    <br>
    <img src="doc_pics/register_await.png" alt="register_await">
    </li>
</ul>
</div>
<footer>
    <p>В приложении использовались иконки <b><a href="https://icons.getbootstrap.com/">Bootstrap icons</a></b></p>
</footer>