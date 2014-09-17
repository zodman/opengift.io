python /vagrant/manage.py schemamigration PManager --auto
python /vagrant/manage.py migrate PManager
supervisorctl reload
