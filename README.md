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
        git clone git@github.com:opengift-io/opengift.io.git opengift

5. Перейдите в папку с проектом и запустите виртуальную машину (В первый раз должен будет скачаться образ.

        vagrant up

6. Для работы нужно указать что opengift.dev является именем ресурса 192.168.33.13.
    Проще всего сделать это в файле hosts.
    
    **Linux**
    
    Добавьте строчку

        192.168.33.13     opengift.srv

    в файл /etc/hosts

     **Windows**
     
     Откройте командную строку в режиме администратора (Правой кнопкой на ярлыке - Запустить от имени администратора).
     Выполните

        notepad %WINDIR%\System32\drivers\etc\hosts

    Добавьте строчку

        192.168.33.13     opengift.srv

7. Когда виртуальная машина запустится выполните в bash терминале

        vagrant provision

8. Rename settings file

        cp /vagrant/tracker/settings.py.dist /vagrant/tracker/settings.py

9. Apply migrations if necessarily.

        cd /vagrant
        python manage.py schemamigration PManager --auto
        python manage.py migrate PManager

10. Откройте в браузере страницу [opengift.srv](http://opengift.srv)
