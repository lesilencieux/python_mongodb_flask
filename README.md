Keep in mind that this is not a complete web application, but a proof of concept on how to make work flask-login with mongoDB (and pymongo).

1. create virtual environnement and activate it by doing
    - mkdir venv
    - virtualenv venv/
    - source venv/bin/activate

2. install pip within environment
    - sudo apt install python3-pip

3. install the requirements librairies 
    - pip install -r requirements.txt
    - pip install python-dateutil

4. add permission to run-dev.py
    - chmod 777 run-dev.py

5. install and run mongo
    - service mongod start

6. run project
    - python3 run-dev.py


You can install everything in a [virtualenv](https://virtualenv.pypa.io/en/latest/) without problems.

Moreover, you need mongoDB to be installed and running.

I included a script (populateDB.py) that you can use to setup the DB with the user and password you want to test.

Last, but not least: generally `config.py` file should not be shared because contains sensitive information, but in this case it's needed to make all work and it's not containing so much ;)

If you have any improvement or suggestion, please let me know!

ok



