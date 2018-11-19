export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

# install deps
sudo apt install -y --force-yes python-dev mysql-server libxml2-dev git libmysqlclient-dev python-pip mysql-server git git-core curl  software-properties-common python-setuptools python-docutils libxml2-dev libxslt-dev redis-server  libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev
# install nodejs
wget -qO- https://deb.nodesource.com/setup_10.x | sudo bash -
sudo  apt install -y nodejs 


sudo pip install -r /vagrant/requirements.txt

echo "drop database if exists tracker" | mysql -u root -proot 
echo "create database tracker" | mysql -u root -proot 

cd /vagrant/

if [ ! -f tracker/settings ]; then
    cp tracker/settings.py.dist tracker/settings.py
fi
if [ ! -f tracker/local_settings.py ]; then
    cp tracker/local_settings.py.ini tracker/local_settings.py
fi 
rm  PManager/migrations/* -rf
mkdir  -p tracker/media/
python manage.py schemamigration PManager --initial
python manage.py syncdb --all --noinput
python manage.py loaddata PManager/fixtures/init_data.json