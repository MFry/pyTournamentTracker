#!/usr/bin/env bash

#Provision PostgreSQL 9.5
apt-get -qq update
# Install the postgres key
echo "Importing PostgreSQL key and installing software"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main 9.5" >> /etc/apt/sources.list.d/pgdg.list
sudo apt-get update
sudo apt-get -y install postgresql-9.5 postgresql-client-9.5 postgresql-contrib-9.5

# Create the user to access the db. (vagrant sample)
sudo -u postgres psql -c "CREATE USER vagrant WITH SUPERUSER CREATEDB ENCRYPTED PASSWORD 'vagrant'"
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb tournament'
su vagrant -c 'psql tournament -f /vagrant/tournament/tournament.sql'
echo "Changing to dummy password"
sudo -u postgres psql postgres -c "ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres'"
sudo -u postgres psql postgres -c "CREATE EXTENSION adminpack";
sudo -u postgres createdb testdb -O postgres

echo "Configuring postgresql.conf"
sudo echo "listen_addresses = '*'" >> /etc/postgresql/9.5/main/postgresql.conf
sudo echo "logging_collector = on" >> /etc/postgresql/9.5/main/postgresql.conf

# Edit to allow socket access, not just local unix access
echo "Patching pg_hba to change -> socket access"
sudo echo "host all all all md5" >> /etc/postgresql/9.5/main/pg_hba.conf

echo "Patching complete, restarting"
sudo service postgresql restart


# sudo -i
#sudo apt-get -qq install synaptic libc6
#apt-get -qq install postgresql
#Remove any older postgresql installation you may have (ex:)
#apt-get -qq remove postgresql postgresql-contrib postgresql-client

#touch /etc/apt/sources.list.d/pgdg.list
#echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
#apt-get install wget ca-certificateswget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
# Install the PostgreSQL
#apt-get -qq install postgresql
#apt-get -qq update