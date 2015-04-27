# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
####Для установки локальной дев копии нужно:

1. Установить VirtualBox ( https://www.virtualbox.org/wiki/Downloads ) 

2. Установить Vagrant ( http://www.vagrantup.com/downloads.html ) 

3. Установить git ( http://git-scm.com/ )

4. В терминале (В Windows можно воспользоваться Git Bash )
   перейдите в папку с проектами. И скачайте репозиторий.
   Например:

        cd /home/user/Projects
        git clone git@bitbucket.org:Gvammer/heliard.git heliard

5. Перейдите в папку с проектом и запустите виртуальную машину (В первый раз должен будет скачаться образ.

        vagrant up

6. Для работы нужно указать что heliard.dev является именем ресурса 192.168.33.13.
    Проще всего сделать это в файле hosts.
    *Linux*
    Добавьте строчку 

        192.168.33.13     heliard.dev

    в файл /etc/hosts

     *Windows*
     Откройте командную строку в режиме администратора (Правой кнопкой на ярлыке - Запустить от имени администратора).
     Выполните

        notepad %WINDIR%\System32\drivers\etc\hosts

    Добавьте строчку

        192.168.33.13     heliard.dev

7. **Теперь машина предоставляется без базы даннах**
 Поэтому необходимо инициализировать базу.
 Скачайте с репозитория файл дампа базы dump.sql в разделе Загрузки 
 и поместите его в директорию проекта. Далее: 

        vagrant ssh
        cd /vagrant
        mysql -u root -p < dump.sql

    Потребуется ввести пароль - введите root 
    (Если долго не будет ответа нажмите Ctrl+C и введите 

        sudo service mysql restart

    и повторите команду.
        
        rm -f dump.sql
        python manage.py schemamigration --initial
        exit

8. Когда виртуальная машина запустится выполните в bash терминале

        vagrant provision

9. Откройте в браузере страницу [heliard.dev](http://heliard.dev)

* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact