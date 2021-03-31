# We import Flask
from flask import Flask, jsonify, request, render_template, Blueprint
from flask_paginate import Pagination, get_page_args, get_page_parameter
import urllib.request
import json
    
# We create a Flask app
app = Flask(__name__)
app.template_folder = ''
users = list(range(10))


#variaveis globais
#urlData = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-sample.json"
urlData = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json"

#Bounding Box Grupo ZAP
minLon = -46.693419
minLat = -23.568704
maxLon = -46.641146
maxLat = -23.546686

#Listas de armazenamento
listZap = []
listViva = []
listExcluidas = []

def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData


def escrever_json(lista):
    with open('meu_arquivo.json', 'w') as f:
        json.dump(lista, f)


    

@app.route('/vivareal', methods=['GET'])
def vivareal():
    jsonData = getResponse(urlData)
    count = 0
    
    print(f'Tamanho do jsonData: ',len(jsonData))
    for i in jsonData:
        #Valores capturados para domada de decisão
        valorImovel = int(i["pricingInfos"]["price"])
        tipoNegocio = i["pricingInfos"]["businessType"]
        longitude = i["address"]["geoLocation"]["location"]["lon"]
        latitude = i["address"]["geoLocation"]["location"]["lat"]
        areaUsada = i["usableAreas"]
    
        #Quando o imovel é venda ou falta o campo condominio
        try:
            condoFree  = int(i["pricingInfos"]["monthlyCondoFee"])
        except NameError as error:
            print(f'Dentro do except')
        except KeyError:
            condoFree = 0
        
         #Variavel de contagem    
        count += 1

        #Verificando se está nas proximidades da OLX
        if minLon <= longitude and maxLon >= longitude and minLat <= latitude and maxLat >= latitude:
            i["pricingInfos"]["price"] = valorImovel + (valorImovel * 0.5)

        if longitude == 0 and latitude == 0:
            listExcluidas.append(i)
        else:
            if tipoNegocio == 'RENTAL' and valorImovel >= 4000 or tipoNegocio == 'SALE' and valorImovel >= 700000:
                listViva.append(i)
            
    totalList = len(listViva)
    print(f'Tamanho da lista: ',totalList)
    escrever_json(listViva)
    #Inicio da paginação
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=totalList, search=True, record_name='users')
    return render_template('index.html',
                           page=page,
                           users=listViva, # O List com as informações
                           per_page=10,
                           offset=0,
                           pagination=pagination,
                           )






# We establish a Flask route so that we can serve HTTP traffic on that route 
@app.route('/')
def weather():
    return 'Olá Mundo! - ZAP'

@app.route("/zap", methods=['GET'])
def zap():
    return 'Olá Mundo! - ZAP'

# Get setup so that if we call the app directly (and it isn't being imported elsewhere)
# it will then run the app with the debug mode as True
# More info - https://docs.python.org/3/library/__main__.html
if __name__ == '__main__':
    app.run(debug=True)
