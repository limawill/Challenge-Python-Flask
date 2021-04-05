from dynaconf import settings             
from cachetools import cached, TTLCache     
from flask import request  
import urllib.request                     
import json


cache = TTLCache(maxsize=20000, ttl=60)

#Listas de armazenamento
listZap = []
listViva = []
listExcluidas = []

@cached(cache)
def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData

def configure(app):
   
   @app.route('/')
   def home():
     return "Sintaxe:   <br><br> 127.0.0.1:5000/vivareal?pageNumber=1&pageSize=2  <br><br> ou <br><br>127.0.0.1:5000/zap?pageNumber=1&pageSize=2"

   
   @app.route('/vivareal', methods=['GET'])
   def vivareal():
      pageNumber = request.args.get('pageNumber')
      pageSize = request.args.get('pageSize')
      jsonData = getResponse(settings.URL)

      for i in jsonData:
         #Valores capturados para domada de decisão
         valorImovel = int(i["pricingInfos"]["price"])
         tipoNegocio = i["pricingInfos"]["businessType"]
         longitude = i["address"]["geoLocation"]["location"]["lon"]
         latitude = i["address"]["geoLocation"]["location"]["lat"]
         areaUsada = i["usableAreas"]
         
         #Quando o imovel é venda ou falta o campo condominio
         try:
            condoFree = int(i["pricingInfos"]["monthlyCondoFee"])
         except NameError as error:
            print(f'Dentro do except')
         except KeyError:
            condoFree = 0

         # Regra de negocio 30%
         condominioCalc =  valorImovel * 0.3
      
        #Verificando variaveis de exlusão automaticas
         if longitude == 0 and latitude == 0:
            listExcluidas.append(i)
         else:
            if settings.minLon <= longitude and settings.maxLon >= longitude and settings.minLat <= latitude and settings.maxLat >= latitude:
               if tipoNegocio == 'RENTAL' and valorImovel >= 6000 and condoFree > 0 and condominioCalc < condoFree or tipoNegocio == 'SALE' and valorImovel >= 700000:
                  listViva.append(i)
            else:
               if tipoNegocio == 'RENTAL' and valorImovel >= 4000 and condoFree > 0 and condominioCalc < condoFree or tipoNegocio == 'SALE' and valorImovel >= 700000:
                  listZap.append(i)

      saidaDados = []
      saidaDados.append({'pageNumber': pageNumber,'pageSize': pageSize,'totalCount': len(listViva), 'listings:': listViva })
      
      return json.dumps(saidaDados)


   

   @app.route("/zap", methods=['GET'])
   def zap():
      pageNumber = request.args.get('pageNumber')
      pageSize = request.args.get('pageSize')
      jsonData = getResponse(settings.URL)
      #count = 0

      for i in jsonData:
         #Valores capturados para domada de decisão
         valorImovel = int(i["pricingInfos"]["price"])
         tipoNegocio = i["pricingInfos"]["businessType"]
         longitude = i["address"]["geoLocation"]["location"]["lon"]
         latitude = i["address"]["geoLocation"]["location"]["lat"]
         areaUsada = i["usableAreas"]
   
         #Quando o imovel é venda ou falta o campo condominio
         try:
            condoFree = int(i["pricingInfos"]["monthlyCondoFee"])
         except NameError as error:
            print(f'Dentro do except')
         except KeyError:
            condoFree = 0
         
       
         
         #Verificando variaveis de exlusão automaticas
         if longitude == 0 and latitude == 0 or areaUsada == 0:
            listExcluidas.append(i)
         else:
            # Verificar o valor do metro quadrado
            verificaVenda = valorImovel/areaUsada  
            #Verificando se está nas proximidades da OLX
            if settings.minLon <= longitude and settings.maxLon >= longitude and settings.minLat <= latitude and settings.maxLat >= latitude:
               if tipoNegocio == 'RENTAL' and valorImovel >= 3500 or tipoNegocio == 'SALE' and valorImovel >= 540000 and verificaVenda > 3500:
                  listZap.append(i)
            else:
               if tipoNegocio == 'RENTAL' and valorImovel >= 3500 or tipoNegocio == 'SALE' and valorImovel >= 600000 and verificaVenda > 3500:
                  listZap.append(i)
      
      saidaDados = []
      saidaDados.append({'pageNumber': pageNumber,'pageSize': pageSize,'totalCount': len(listZap), 'listings:': listZap })
      
      return json.dumps(saidaDados)
