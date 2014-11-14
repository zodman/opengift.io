ssh-keygen -t rsa -f ~/.ssh/id_rsa
cd ~
git clone git://github.com/sitaramc/gitolite
mkdir -p ~/bin
gitolite/install -ln ~/bin
gitolite setup -pk ~/.ssh/id_rsa.pub