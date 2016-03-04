apt-get -qq update
apt-get -qq install postgresql
# echo
apt-get -qq install python-virtualenv
apt-get -qq install libpq-dev libreadline-dev libsqlite3-dev libssl-dev
# python3-dev
# apt-get -qq install build-essential checkinstall
cd /usr/src
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
sudo tar xzf Python-3.5.1.tgz
cd python-5.5.1
sudo ./configure
sudo make altinstall
# vsudo -u vagrant virtualenv -p /usr/bin/python3 py3env
# source py3env/bin/activate
# cd /vagrant/tournament
# sudo -u vagrant pip install -r requirements.txt

vagrantTip="[35m[1mThe default synced directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
#Ref: https://gist.github.com/dwayne/87f807f0d313b444bb37
#Ref: http://tecadmin.net/install-python-3-4-on-ubuntu-and-linuxmint/#
#Ref: http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi