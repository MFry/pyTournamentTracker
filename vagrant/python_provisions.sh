#!/usr/bin/env bash

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

echo 'Clean up...'
cd && rm -rf /tmp/Python-3.5.1