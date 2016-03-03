apt-get -qqy update
virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
pip install package-name
apt-get -qqy install postgresql python3-psycopg2
apt-get -qqy install python3-pip
apt-get -qqy install python3-flask python3-sqlalchemy

vagrantTip="[35m[1mThe default synced directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
