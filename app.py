from flask import Flask, request
from flask import jsonify
import views

def create_app():
    app = Flask(__name__)
    views.configure(app)
    return app


# Rodar no terminal
# export FLASK_ENV=development
# export FLASK_APP=app:create_app

# Verifique
#env | grep FLASK_

#Executar
#flask run

#Instalei
# pip install python-dotenv
# python-dotenv==0.17.0

#pip install Flask
#Flask==1.1.2
#flask-paginate==0.8.1
#flask-restplus==0.13.0

#pip install dynaconf
# dynaconf==3.1.4

# pip install cachetools 
# cachetools==4.2.1

# pip install urllib3
# urllib3==1.25.7

# pip install jsons
# jsons==1.4.1
