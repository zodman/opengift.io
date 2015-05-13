#!/bin/bash
# Принимает имя проекта и порт
name=$1
port=$2

domain=$name".heliard.ru"
block="/etc/nginx/sites-available/heliard" # Уточнить путь к конфигу nginx
# Если новый файл конфига к каждому поддомену 
# block="/etc/nginx/sites-available/$domain"

config=$(cat <<"EOF"
\n
server {\n
	\tserver_name $domain;\n
	\tlocation / {\n
		\t\tproxy_redirect off;\n
		\t\tproxy_set_header Host \$host;\n
		\t\tproxy_set_header X-Real-IP \$remote_addr;\n
		\t\tproxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;\n
		\t\tproxy_pass http://localhost:$port;\n
	\t}\n
}
EOF
)

echo $config >> $block

# Если новый файл конфига к каждому поддомену
# ln -s $block /etc/nginx/sites-enabled/ 

service nginx reload

exit 0