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

# Run the web server
  
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

## Run the web server via gunicorn

If we want to use gunicorn, we can also run below command:

    $ MONGODB_URI=mongodb://localhost:27017 REDIS_URI=redis://localhost:6379/0 MEMCACHED_URI=localhost:11211 gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" --workers=2 --bind=localhost:8080 app:app --daemon --pid /tmp/smart-web.pid

It's simple for us to start multiple processes and serve on the same port.

# Run the worker server

- One node worker server

    Run below command to start one node of worker:

        $ REDIS_URI=redis://localhost:6379/0 celery worker --app=smartworker.worker:worker

    or if you want to use different cocurrent pool instead of default processes

        $ REDIS_URI=redis://localhost:6379/0 celery worker --app=smartworker.worker:worker -P gevent -c 1000

- Multi nodes of worker server

    Run below command to start 4 nodes of workers (in case the server has 4 CPUs):

        $ REDIS_URI=redis://localhost:6379/0 celery multi start 4 --app=smartworker.worker:worker -P gevent -l info -c:1-4 1000

# Run periodic task server

**Make sure only one node is running the periodic task.** Run below command to start the periodic task server:

    $ REDIS_URI=redis://localhost:6379/0 celery beat --app=smartworker.worker:worker --pid=/tmp/periodic_task.pid --detach
