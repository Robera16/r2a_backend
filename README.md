# r2a_backend
Right to Ask Django Backend API service

## Prerequisite :mask:
  1. ```python 3.6```
  2. ```postgresql ```
  3. ```pip version (20.0.2) python 3.6```
  4. ```pip install virtual env```
  4. ```create database r2a_development as postgres and grant all permissions``` (can be modified from dev_envs.sh)
  5. ``` configure dev_envs.sh to configure db functions and other env driven functions``` (not harcoding creds other stuff) we use ```.env.prod``` on production
  
  
## Setup :fire:
  1. ```virtualenv  --python=python3 venv``` 
  2. ```source venv/bin/activate```
  3. ```pip install -r requirements.txt```  ->  ```(sudo apt-get install libpq-dev ) if psycopg2 installation fails ```
  4. ```source dev_envs.sh```
  5. ```python manage.py migrate```
  6. ```python manage.py loaddata api_auth/load_user_meta.json``` (not mandatory)
  7. ```python manage.py createsuperuser``` (creates a superuser,  can login at localhost:8000/admin)
  7. ```python manage.py runserver ``` (runs server on localhost:8080)

## Deployment :rocket:
  1. ssh to the ec2 box with ```ssh -i r2a_prod.pen ec2-user@15.207.87.156``` and  ```cd r2a_backend``` 
  2. configure git and pull changes
  3. ```docker-compose -f docker-compose-production.yaml down``` (stops the application)
  4. ```docker-compose -f docker-compose-production.yaml up --build -d``` (restarts the application)
  5. ```docker-compose -f docker-compose-production.yaml exec web python manage.py migrate``` (run migrations if any)  

[End points list](https://github.com/charithreddyv/r2a_backend/blob/master/ENDPOINTS.md)
