#!/bin/bash

echo "Limpando terminal:"
clear;
echo "Setando variaveis do ambiente:"
export FLASK_ENV=development;
export FLASK_APP=app:create_app;
echo "Verificando:"
env | grep FLASK_
echo "Start Flask:"
flask run