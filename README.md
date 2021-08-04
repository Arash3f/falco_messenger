# What is Falco Messenger ?
As it's obvious from the name of the project , it's a messenger which created by the combination of Django and Channels library and there is bootstrap framework at the frontend.
- [Features](https://github.com/Arash3f/falco_messenger#features)
- [How to Deploy ?](https://github.com/Arash3f/falco_messenger#how-to-deploy-)
- [Deploy with Python Environment ](https://github.com/Arash3f/falco_messenger#python-environment)
- [Deploy with Docker ](https://github.com/Arash3f/falco_messenger#docker)

## Features
It has been tried to have the real messenger features , and among the features of this messenger, the following can be mentioned
- login
- logout
- register
- edit user informations
- create group
- remove group
- join group
- see group information
- kick user from group
- warning message
- live chat

>**Note** : For this project , The docker-compose file has been created so that you can deploy the project with nginx.

# How to Deploy ?
We have 2 ways to deploy this project  :
1. Python Environment
2. Docker

## Python Environment
**Clone project :**

- `git clone https://github.com/Arash3f/Django-Portfolio.git`

- `cd falco`

- `cd project`

**Create environment**

- `python3 -m venv venv`

**Active environment**

- linux : `source venv/bin/activate`

- windows : `.\venv\Scripts\activate`

**Install libraries**

- `pip3 install -r requirements.txt`

**Staticfiles**

- `python3 manage.py collectstatic`

**makemigrations/migrate**

- `python3 manage.py makemigrations`

- `python3 manage.py migrate`

**redis config**

-  in settings.ini file you can change REDIS_HOST to your host name

**run project**

- `daphne -b 0.0.0.0 -p 8000 falco.asgi:application`

> project is running on port **8000** with **Daphne**

## Docker
> if befor now  collect staticfile , remove it first

> Ports **6379**, **8000**, and **80** must be free

**Clone project**

- `git clone https://github.com/Arash3f/Django-Portfolio.git`
- `cd falco`

**run project**

- `sudo docker-compose run -d --build`

> project is running on port **80**  with **Dephne**

> project is running on port **8000**  with **Dephne** and **Nginx**
