apt-get -qqy update
apt-get -qqy install postgresql
apt-get -qqy install python3
apt-get -qqy install python-virtualenv
apt-get install libpq-dev python3-dev
sudo -u vagrant virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
cd /vagrant/tournament
sudo -u vagrant pip install -r requirements.txt

vagrantTip="[35m[1mThe default synced directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
