#!/bin/bash
# Принимает имя проекта и порт, который нужно пробросить, дистрибутив
name=$1
port=$2
distro=$3
#username=$4
#identity=$5


cd /home/$name
touch Dockerfile

echo "FROM $distro" >> Dockerfile
echo "EXPOSE $port" >> Dockerfile

##################### Not needed yet ###################################################################
#echo "RUN mkdir /home/$username" >> Dockerfile
#echo "RUN mkdir /home/$username/.ssh" >> Dockerfile
## Если публичный ключ передается строкой
#echo "RUN touch /home/$username/.ssh/id_rsa.pub" >> Dockerfile
#echo "RUN echo $identity >> /home/$username/.ssh/id_rsa.pub" >> Dockerfile
#
#echo "RUN sed -i -e '/^PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config" >> Dockerfile
#echo "RUN restart ssh" >> Dockerfile
#######################################################################################################

docker build -t hub:$name /home/$name # вместо hub должно стоять имя хаба гелиарда
docker run -d -P -t --name $name --restart=always -v /home/$name:/project hub:$name # вместо hub должно стоять имя хаба гелиарда

exit 0