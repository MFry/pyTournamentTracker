apt-get -qqy update
virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
pip install package-name
apt-get -qqy install postgresql python3-psycopg2
apt-get -qqy install python3-pip
apt-get -qqy install python3-flask python3-sqlalchemy
