# Grupo ZAP
## Code Challenge Grupo ZAP

Este projeto é executado no micro framework Python: Flask.

## Dependencias

- dynaconf==3.1.4
- Flask==1.1.2
- cachetools==4.2.1
- python-dotenv==0.17.0
- urllib3==1.25.7

## Como rodar localmente?
O Software foi desenvolvido no linux  Fedora 32, para rodar o app primeiramente precisamos instalar suas dependencia (que foram listadas acima), se estiver utilizando um ambiente virtual remover o --user:
```sh
pip install Flask --user;
pip install python-dotenv --user;
pip install dynaconf --user; 
pip install cachetools --user; 
pip install urllib3 --user; 
pip install jsons --user;
```
Setar variaveis do ambiente:
```sh
export FLASK_ENV=development;
export FLASK_APP=app:create_app;
```
Caso queira verificar: 
```sh
env | grep FLASK_ ;
```
E iniciar o Flask
```sh
flask run
erro python linux não reconhece comando pip```
#### Rodar script
Outra opção é executar o arquivo configure.sh (raiz do projeto), conteúdo do arquivo:
```sh
#!/bin/bash

echo "Limpando terminal:"
clear;
echo "Setando variaveis do ambiente:"
export FLASK_ENV=development;
export FLASK_APP=app:create_app;
echo "Verificando:"
env | grep FLASK_ ;
echo "Start Flask:"
flask run

```
Para executar

```sh
$ chmod a+x configure.sh
$ ./configure.sh
```
## Como rodar os testes
Após o flask estar ativo acesse:
```sh
http://127.0.0.1:5000
```
Irá aparecer na tela a maneira de como deve ser acessado cada resultado, para o Grupo ZAP E VIVA REAL

Um exemplo da URL de acesso do ZAP:
```sh
http://127.0.0.1:5000/zap?pageNumber=1&pageSize=20
```
Viva Real
```sh
http://127.0.0.1:5000/vivareal?pageNumber=8&pageSize=70
```

## Como fazer o deploy?

Para realizar o deploy digite a url:
```sh
http://127.0.0.1:5000/vivareal?
```
ou
```sh
http://127.0.0.1:5000/vivareal?
```
Acrescentando as iformações solicitadas:
```sh
pageNumber e pageSize
```

## Estrutura do projeto
.
├── app.py                                      
├── configure.sh
├── README.md
├── settings.toml
└── views.py
