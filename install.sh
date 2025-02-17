
echo "deb https://dl.bintray.com/questdb/stable questdb main" | tee /etc/apt/sources.list.d/questdb.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0x7F8B3D5D
apt-get update
apt-get install questdb
systemctl start questdb