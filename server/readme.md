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

    $ nosetests test

# Run the server
  
We defines below env variables:

- MONGODB_URI: mongodb://localhost:27017
- MONGODB_REPLICASET: mongo replicaset name. *TODO: necessary?*
- REDIS_URI: redis://localhost:6379
- MEMCACHED_URI: localhost:11211
- WEB_HOST and WEB_PORT: hostname and port of the web server

Start server using below command:

    $ python app.py

It will read configuration from environment, and use default in case of no defination in environment.

Or we can define env in command line:

    $ MONGODB_URI=mongodb://localhost:27017 REDIS_URI=redis://localhost:6379 MEMCACHED_URI=localhost:11211 WEB_PORT=8080 python app.py

# Run the server via gunicorn

If we want to use gunicorn, we can also run below command:

    $ MONGODB_URI=mongodb://localhost:27017 REDIS_URI=redis://localhost:6379 MEMCACHED_URI=localhost:11211 gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" --workers=2 --bind=localhost:8080 app:app

It's simple for us to start multiple processes and serve on the same port.
