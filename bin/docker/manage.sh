#!/bin/bash
# Принимает имя проекта, ссылку на гит, дистрибутив
# имя юзера, public_key

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

dir=$(dirname $0)
name=$1
git=$2
distro=$3 # Например ubuntu:14.04.2
ports=$dir/ports
#username=$5
#identity=$6

last_port=$(tail -n 1 $ports)
port=$((last_port + 1))
echo $port >> $ports
echo $port

# Имена остальных скриптов
folders="$dir/folder_master.sh"
nginx="$dir/nginx_config.sh"
docker="$dir/docker_master.sh"

$folders "$name" "$git"
$nginx "$name" "$port"
$docker "$name" "$port" "$distro" #$username $identity

exit 0