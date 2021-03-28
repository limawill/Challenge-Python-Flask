import pandas as pd
import json
import pprint 
import urllib.request
import requests
import sys

#    Ele apenas é elegível pro portal ZAP:
#        Quando for aluguel e no mínimo o valor for de R$ 3.500,00.
#        Quando for venda e no mínimo o valor for de R$ 600.000,00.
#    Ele apenas é elegível pro portal Viva Real:
#        Quando for aluguel e no máximo o valor for de R$ 4.000,00.
#        Quando for venda e no máximo o valor for de R$ 700.000,00.

# Variavél que recebe a massa de dados
url = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json"


#Função responsável pela abertura e verificação de acesso aos dados
def ler_json(arq_json):
    acessoPagina = requests.get(arq_json)
    if acessoPagina.status_code >= 200:
        with urllib.request.urlopen(arq_json) as response:
            return response.read()
    else:
        print("Erro de acesso aos dados")
        sys.exit([acessoPagina])


data = ler_json(url)

#Listas de armazenamento
listCasa1 = []
listCasa2 = []



for item in data:
    tipoManga = item['pricingInfos']['businessType']
    price = int(item['pricingInfos']['price'])
    longitude = item['address']['geoLocation']['location']['lon']
    latitude = item['address']['geoLocation']['location']['lat']

    if longitude != 0 and latitude !=0:
      if tipoManga == 'RENTAL' and price >= 3500 or tipoManga == 'SALE' and price >= 600000:
        listCasa1.append(item)

        if tipoManga == 'RENTAL' and price >= 4000 or tipoManga == 'SALE' and price >= 700.000:
          listCasa2.append(item)
    else:
      print ("Temos 1")

print(listCasa1)
print(listCasa2)