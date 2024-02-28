# Flight service API
This is a simple flight service API. It is built using Django and Django Rest Framework.

## Installation
Install PostgreSQL and create a database.

```
git clone https://github.com/antonnech2309/flight_service.git
cd flight_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set POSTRGES_HOST=<your db host name>
set POSTRGES_DB=<your db name>
set POSTRGES_USER=<your db user>
set POSTRGES_PASSWORD=<your db password>
SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Run with docker
```
docker-compose build
docker-compose up
```

## Getting access

- create user via /api/user/register/
- get access token via /api/user/token/