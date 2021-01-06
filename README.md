# Example integration of Flask-Meld + Flask-SocketIO

Existing Flask-SocketIO users may have taken notice of a recent up-and-comer project called Flask-Meld which allows for a more pythonic approach to creating dynamic front-ends in your Flask project. This example is created to demonstrate a broad edge case for existing Flask-SocketIO users to integrate Flask-Meld, taking advantage of uWSGI behind NGINX. A special thanks to @mikeabrahamsen for dynamically supporting this integration effort.

# Assumptions

This example makes the following assumptions
* You have an existing Flask-SocketIO project
* Your project is driven with deployed with uWSGI
* Your project is served with NGINX
* Your project is used in a virtual python enviroment (3.8.x or higher)

# Demonstrates

This example makes the following demonstrations
* You can safely integrate Flask-Meld without disruption of your existing SocketIO
* This configuration is compatible with Cloudflare DNS (Proxy)
* This configuration is compatible with both local NGINX and remote NGINX(reverse proxy) websockets
* This configuration is compatible with both secure and insecure websockets

# Requirements
uWSGI SSL requires pcre libraries to support secure websocket handshake 
> (related error "!!! no internal routing support, rebuild with pcre support !!!)

with apt packager
```bash
sudo apt-get install libpcre3 libpcre3-dev
```

# Getting Started

* Clone this repository

```bash
git clone <this_repository>
```

* Initiate this project and activate virtual python enviroment
```bash
<pip_venv_instructions>
```
> or with pipenv
```bash
pipenv install -r requirements.txt

pipenv shell
```

* 

At this point you can start your uWSGI server to validate local Meld and SocketIO websockets individually
* launch uWSGI
```bash
uwsgi --http :8080 --gevent 1000 --http-websockets --master --wsgi-file wsgi.py --callable app
```

You can now open your browser and point it towards 127.0.0.1:8080 or <YOUR_IP:8080> and test functions


# NGINX Configuration
<NGINX_configuration>


# Example TODO

## Finish documentation
## Implement a create_app() demonstration vs ./app.py starter