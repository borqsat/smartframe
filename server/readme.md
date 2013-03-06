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

Create a product configure file `product.ini` under current directory firstly,
and then run below command:

    $ python app.py -c product.ini

There is already a development config file `development.ini`, you can modify
it per your server's confiuration.
