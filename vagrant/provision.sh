#!/usr/bin/env bash
apt-get -qq update
sudo -i
sudo apt-get -qq install synaptic libc6
#apt-get -qq install postgresql
# Remove any older postgresql installation you may have (ex:)
# apt-get -qq remove postgresql postgresql-contrib postgresql-client

touch /etc/apt/sources.list.d/pgdg.list
echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
sudo apt-get install wget ca-certificateswget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# Install the PostgreSQL
apt-get -qq install postgresql
apt-get -qq update

# Create the user to access the db. (vagrant sample)
sudo -u postgres psql -c "CREATE USER vagrant WITH SUPERUSER CREATEDB ENCRYPTED PASSWORD 'vagrant'"
# echo
apt-get -qq install python-virtualenv
apt-get -qq install libpq-dev libreadline-dev libsqlite3-dev libssl-dev
# python3-dev
apt-get -qq install build-essential checkinstall
cd /tmp
wget -O- -q https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz | tar xz
cd Python-3.5.1
./configure
make -s
make -s altinstall
sudo -H pip3.5 install --upgrade pip
sudo -H pip3.5 install virtualenvwrapper
virtualenv --no-site-packages /vagrant/tournament/virtualenv/
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb tournament'
su vagrant -c 'psql tournament -f /vagrant/tournament/tournament.sql'

#source /vagrant/tournament/virtualenv/bin/activate
#cd /vagrant/tournament/
#sudo -H pip install -r requirements.txt
#sudo -u vagrant virtualenv -p /usr/bin/python3 py3env
#source py3env/bin/activate

# cd /vagrant/tournament
# sudo -u vagrant pip install -r requirements.txt

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

#Ref: https://gist.github.com/dwayne/87f807f0d313b444bb37
#Ref: http://tecadmin.net/install-python-3-4-on-ubuntu-and-linuxmint/#
#Ref: http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi
#Ref: https://iamzed.com/2009/05/07/a-primer-on-virtualenv/
#Ref: http://www.simononsoftware.com/virtualenv-tutorial-part-2/