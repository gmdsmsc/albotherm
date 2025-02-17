
chmod +x install.sh

wget https://questdb.com/download/questdb-8.2.2-rt-linux-x86-64.tar.gz -O questdb.tar.gz

tar -xvf questdb-8.2.2-rt-linux-x86-64.tar.gz -C $HOME/.questdb
cd $HOME/.questdb
./questdb.sh start
