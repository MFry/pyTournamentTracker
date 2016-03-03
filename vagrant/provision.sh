apt-get -qqy update
apt-get -qqy install postgresql
virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
cd /vagrant/tournament
pip install -r requirements.txt

vagrantTip="[35m[1mThe default synced directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
