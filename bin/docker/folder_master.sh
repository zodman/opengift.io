#!/bin/bash
# Принимает имя проекта и ссылку на гит
name=$1
git=$2

# Папки для проекта
mkdir /home/$name

cd /home/$name
git clone $git

# База данных
#dbuser="root"
#dbname=$name
#dbpassword="root"
#dbdir="/home/$name/db"
#mysql -e "create database \`$dbname\`; grant all on \`$dbname\`.* to '$dbuser'@'localhost'; set password for #'$dbuser'@'localhost' = password('$dbpassword');"

#service mysql reload

# crontab
crontab -l > cron
echo "*/5 * * * * cd /home/$name && git pull && docker stop $name && docker start $name" >> cron
crontab cron
rm cron

exit 0