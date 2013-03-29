# Prerequirement

- Ubuntu 12.04
- Python 2.7

# Installation

-   Libraries

    Before installing python packages, we must make sure next libraries are installed: libsssl, python-dev, livevent.

        $ sudo apt-get install libssl-dev python-dev libevent-dev

- Python Packages. It's strongly recommended to install python packages using virtual environment.

        $ pip install -r requirements.txt --use-mirrors

- Virtual environment

    We have a script to setup virtual env in one step:

        $ ./setup.sh

    Activate the virtual env

        $ . venv/bin/activate

- Servers for development 
    
     Before running the server, you must set up `mongodb`, `memcached`, `redis` on your local PC.

        $ sudo apt-get install mongodb memcached redis-server

# Run the test

        $ nosetests

# Run the server
  
- Read configuration from config file: `development.ini`.

        [redis]
        uri=redis://localhost:6379

        [mongodb]
        uri=mongodb://localhost:27017
        replicaSet=ats_rs                 --> remove this ling

        [memcached]
        uri=localhost:11211

        [server:web]
        host=localhost
        port=8080
    
    Start server like below:

        $ python app.py -c development.ini

- Read configuration from environment.

    We defines below env variables:

    - MONGODB_URI: mongodb://localhost:27017
    - MONGODB_REPLICASET: mongo replicaset name. *TODO: necessary?*
    - REDIS_URI: redis://localhost:6379
    - MEMCACHED_URI: localhost:11211
    - WEB_HOST and WEB_PORT: hostname and port of the web server

    Start server using below command:

        $ python app.py

    It will read configuration from environment, and use default in case of no defination.
    
    Or we can define env in command line:

        $ MONGODB_URI=mongodb://localhost:27017 REDIS_URI=redis://localhost:6379 MEMCACHED_URI=localhost:11211 WEB_HOST=localhost WEB_PORT=8080 python app.py
