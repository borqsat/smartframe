*) below python environment recommanded
   (a)  python 2.6
   (b)  python-dev 
   (c)  python-installer -> easy_install

1) Install the libevent module (don't use ubuntu "apt-get" to install, in that way we will get the old version)
   (a) download from official site: http://libevent.org/
   (b) unzip libevent package
   (c) cd libevent dir
   (d) ./configure --program-prefix=/usr
   (e) sudo make
   (f) sudo make install

2) Install greenlet package      
   (a) sudo easy_install greenlet

3) Install gevent package
   (a) sudo easy_install gevent

4) Install gevent-websocket package
   (a) sudo easy_install gevent-websocket


*) export to the envrionment PATH
   (a)export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
