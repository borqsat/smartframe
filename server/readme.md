For development purpose

# Installation

- Virtual environment
    
    If you use Ubuntu10.04, please install libssl-dev, 
    After installed successfully, build and install python2.7.

        $ sudo apt-get install libssl-dev

    Enter the directory, and then run below command:

        $ ./setup.sh

    Activate the virtual env

        $ . venv/bin/activate

- Install server tools 
    
     Before running the server, you must set up `mongodb`, `memcached`,
     `redis` on your local PC.

       $ sudo apt-get install mongodb memcached redis-server


# Run the server
  
- Update config file `development.ini`.

    [redis]
    host=192.168.1.96  --> set to 127.0.0.1
    port=6379
    db=0

    [mongodb]
    uri=mongodb://192.168.5.60:27017  --> set to mongodb://127.0.0.1:27017
    replicaSet=ats_rs                 --> remove this ling

    [memcached]
    uri=192.168.7.212:11211           --> set to 127.0.0.1:11211

    [server:web]
    host=localhost
    port=8080

- Start server

     Run command like below:
    
     $ python app.py -c development.ini -d

