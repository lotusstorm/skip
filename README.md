# skip_table 

## инструкция для LINUX !!!

## Выполняем последовательно

#### устанавливаем зависимости для сервиса
```
pip install -r requirements.txt

sudo apt install curl
```
 
#### устанавливаем и настраиваем nginx
```
cd ~
sudo apt-get install nginx
```

#### создаем директории
```
sudo mkdir /etc/nginx/sites-available
sudo mkdir /etc/nginx/sites-enabled
```

#### открываем конфигурационный файл
```
sudo nano /etc/nginx/nginx.conf

если в файле нету этой строчки то добавить
include /etc/nginx/sites-enabled/*;

закоментировать эту строчку
#include /etc/nginx/conf.d/*.conf;

вместо <nginx> написать название пользователя (echo $USER)
user <nginx> www-data;
```

#### создаем конфиг для запуска сервера
```
sudo nano /etc/nginx/sites-available/название_проекта
```

#### содержимое конфиг файла /etc/nginx/sites-available/название_проекта
```
server {
    listen 7887;
    server_name localhost;
 
    location = /favicon.ico { access_log off; log_not_found off; }
 
    location / {
        root /var/www/dist;
        index index.html;
    }
}
```

#### создаем ссылку на конф файл в папке которая отслеживается сервером nginx
```
sudo ln -s /etc/nginx/sites-available/название_проекта /etc/nginx/sites-enabled
```

#### проверяем конфигурационный файл на синтаксические ошибки
```
sudo nginx -t <- выводит в консоль все ошибки
sudo service nginx configtest <- выводит в консоль только статус проверки [OK] или [fail]
```

#### подгружает для сервера новые конфигурации
```
sudo service nginx restart
```

#### установка сборщика пакетов и сборка клиента для продакшена
```
sudo ./install_and_build.sh
```

#### создание и миграция базы данных 
```
./migrate.sh
```

### запуск и остановка сервиса для скипов
``` 
запуск
./start.sh
 
остановка
./stop.sh
```

# API

##### Добавление ветки в бд
тип запроса - ***POST***

url - <http://ip_addres:port/api/global_requests>>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```

возможные варианты для названия веток ***(development, an-minor, an-weekly)***
возможные варианты для названия ос ***(windows, linux)***

##### Обновление ветки в бд
тип запроса - ***PUT***

url - <http://ip_addres:port/api/global_requests>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***

##### Удаление ветки из дб
тип запроса - ***DELETE***

url - <http://ip_addres:port/api/global_requests>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***
возможные варианты для названия ос ***(windows, linux)***

##### Обновление привязанных багов у теста и всех его шагов 
тип запроса - ***POST***

url - <http://ip_addres:port/api/test/update>
```
{
    "id": "идентификатор теста(абсолютный путь который включает в себя и название класса в тесте)",
    "branch": "название_ветки"
    "os": "название_ос"
}
```

пример id - ***blocker.35-Activation-utility.license-review.test.TestActivationUtility***
возможные варианты для названия веток ***(development, an-minor, an-weekly)***
возможные варианты для названия ос ***(windows, linux)***

##### Добавление багов в бд из JIRA
тип запроса - ***POST***

url - <http://ip_addres:port/api/issues>
```
{ 
    "projects": ["ACR"],
    "statuses": ["dev.Open"]
}
```
projects - ***[список, проектов, через, запятую]***

statuses - ***[список, статусов, через, запятую]***

Получение всех багов из бд
тип запроса - ***GET***

url - <http://ip_addres:port/api/issues>

##### Удаление всех багов из бд
тип запроса - ***DELETE***

url - <http://ip_addres:port/api/issues>

##### Обновление всех багов в бд
тип запроса - ***PUT***

url - <http://ip_addres:port/api/issues>

##### Получение всех steps из бд
тип запроса - ***POST*** 

url - <http://ip_addres:port/api/steps>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***

##### Получение всех tests из бд
тип запроса - ***POST*** 

url - <http://ip_addres:port/api/tests>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***

##### Получение всех categories из бд
тип запроса - ***POST*** 

url - <http://ip_addres:port/api/categories>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***

##### Получение всех components из бд
тип запроса - ***POST*** 

url - <http://ip_addres:port/api/components>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***

##### Получение всех modules из бд
тип запроса - ***POST***

url - <http://ip_addres:port/api/modules>
```
{
    "branch": "название_ветки"
    "os": "название_ос"
}
```
возможные варианты для названия веток ***(development, an-minor, an-weekly)***

возможные варианты для названия ос ***(windows, linux)***