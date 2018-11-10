# OpenGift.io

GET SOFTWARE 
DEVELOPMENT SERVICES  
UP TO 10 TIMES CHEAPER 
AND FASTER  

#### DEVELOPMENT StarterKIT

1. Download VirtualBox ( https://www.virtualbox.org/wiki/Downloads )

2. Download Vagrant ( http://www.vagrantup.com/downloads.html )

3. Download git ( http://git-scm.com/ )

4. Clone the project

        cd /home/user/Projects
        git clone git@github.com:opengift-io/opengift.io.git opengift

5. Start vagrant up

        vagrant up --provision

this will install all packages necesary to run from zero  
take a look to provision.sh to see all deps
** vagrant provision will drop your database and recreate a new one **

6.- Run the runserver

        vagrant ssh 
        cd /vagrant
        python manage.py runserver 0:8000


Open your firefox/chrome with http://localhost:8000

you can visit the admin http://localhost:8000/admin/ 
access: admin/admin

its done ready to hack!

** Plus run new unittest:
        fab test

## TODO:
- [ ] add running async_server (websockets) 
- [ ] run blockchain  local (wallet didnt work right now) So when register a user by pass the wallet
