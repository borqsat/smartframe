# Installation

-   libevent-dev

    As python gevent needs libevent-dev, so we must install the lib firstly.

        $ sudo apt-get install libevent-dev

- Virtual environment

    Enter the directory, and then run below command:

        $ ./setup.sh

    Activate the virtual env

        $ . venv/bin/activate

# Run the server

Before running the server, you must set up `mongodb`, `memcached`, `redis`,
and update server config file `product.ini`, just like `development.ini`.
Finally you can execute below command to start the server:

    $ python app.py -c product.ini

You can add `-d` option to use development options. By default, the server
will use replicaset when connecting to mongodb. For development purpose, you
only need to connect to a single mongodb, so you can run command like below:

    $ python app.py -c development.ini -d
