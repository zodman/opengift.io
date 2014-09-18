cp /vagrant/supervisor/vagrant.conf /etc/supervisor/conf.d/heliard.conf
supervisorctl reload
python /vagrant/manage.py schemamigration PManager --auto
python /vagrant/manage.py migrate PManager
service nginx restart
service mysql restart