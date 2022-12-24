## Лабораторные работы по ТРПО

#### [Класс HTTP](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/HTTP.cpp)

Позволяет с помощью CGI и apache2 выполнять такие действия, как:

1. Получение параметров GET и POST запроса - httpPost(), httpGet()
2. Получение и установка Cookie - getCookie(), setCookie()
3. Отправка предварительно созданного файла в браузер (Дополнительно) - httpSendFile()

#### [Класс DB](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/db.cpp)

Предназначен для работы с NoSQL key=value базой данных

Хранение БД производится в файле, внутри программы - это std::set

Реализованные функции:

1. Добавление записи - write()
2. Удаление записи - erase()
3. Просмотр списка записей - read_all()
4. Просмотр одной записи - read_one()

+ [working_with_db.cpp](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/working_with_db.cpp)

#### Задание

* Разработать библиотеку, способную принимать данные методами GET/POST и работать с HTTP-Cookie.
* Написать CGI-программу, использующую разработанную библиотеку и реализующую работу с базой данных со следующими CGI-сценариями:

Добавление записи, удаление, просмотр списка, просмотр одной записи. Сохранить
предыдущие введённые данные в форме добавления записи в Cookie.

* Записи в базе данных хранятся построчно в файле, а отдельные поля записи разделены символами-разделителями.
* Ограничения: Использование только стандартных библиотек. Использовать Boost  и др. библиотеки не допускается. Можно: STL и C++17.

## Лабораторная работа №2

#### Задание

Написать метод rawURLDecode(), который декодирует строку в формате application/x-www-form-urlencoded в нормальное представление;

Вызывать данный метод для всех данных, для которых необходимо преобразование;

Пояснение: строка %D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82%2C%20%D0%BC%D0%B8%D1%80%21

Обозначает фразу «Привет, мир!»

Кириллица занимает 2 байта, символы «,», пробел, и «!» по 1-му байту.

#### Изменения:

В Класс HTTP добавлен метод rawURLDecode:

https://github.com/Nomiram/Cpp-CGI-apache2/blob/70ca72d5576be5f97e88675a14612f7de647d72f/HTTP.cpp#L138

а так же некоторые служебные методы.

## Лабораторная работа №3

#### Задание

Дополнить библиотеку [HTTP.h](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/HTTP.hpp) следующими методами: 

``` C++
std::string getHeader(std::string name);
// возвращает значение HTTP-заголовка “name”
std::string rawURLDecode(std::string name);// декодирует строку из 16-ричного представления в plain-text
UploadedFile getFile(std::string name); 
// возвращает свойства файла “name”
int move_uploaded_file(UploadedFile tmpFile, std::string path); 
// загружает файл “tmpFile” в директорию “path”
```
 * Написать [скрипт](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/working_with_files.cpp), позволяющий загружать несколько файлов в отдельную директорию на сервере. Выбрать MIME-тип содержимого и максимальный размер.
 * Создать [скрипт](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/watch_files.py) для вывода файлов на экран с возможностью удаления любого файла.
 * Предусмотреть [защиту от взлома](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/.htaccess).

Изменения:

1. [working_with_files.cpp](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/working_with_files.cpp)

2. Определение типа в POST запросе и обработка

https://github.com/Nomiram/Cpp-CGI-apache2/blob/82abe5bda9406fcb15ba126f67ed38c700b58e60/HTTP.cpp#L122

## Лабораторная работа №4

#### Задание

 * Ключ сессии, сохраняемый в Cookie, именуется уникальным идентификатором через uuid().
 * Значения сессии хранятся внутри сервера в NoSQL базе данных. В качестве таковой предлагается Redis
 * Значения сериализуются с ключом сессии

Изменения:

[session.py](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/session.py)

## Лабораторная работа №5

#### Задание

Разработать [сервер](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/tcp-server.py), который будет обрабатывать данные по протоколу HTTP. 

Изменения:

[tcp-server.py](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/tcp-server.py)

## Инструкции по запуску:

1. git clone
2. Использовать команды описанные для каждой системы [здесь](https://github.com/Nomiram/Cpp-CGI-apache2/blob/master/run_server.txt)

#### Зависимости: 

Требется установленный docker
