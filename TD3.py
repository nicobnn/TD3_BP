# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:42:09 2020

@author: Nicolas
"""

import requests,json,sqlite3
#list of all available cryptocurrencies displayed in a list
def ShowCurrencies():
    currencies = requests.get('https://api.pro.coinbase.com/products')

    r_json = json.loads(currencies.text)
    all_currencies = []
    for i in r_json:
        all_currencies.append(i['base_currency'])#On met dans la liste que les élements du json avec comme paramètre: base_currency
    
    List_currencies=list(set(all_currencies))#enlever les doublons
    List_currencies.sort()#trier la liste
    #print(List_currencies)

ShowCurrencies()
#function to display the ask or bid price of an asset
def getDepth(direction, pair):
    
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/book'
    BidOrAsk = requests.get(str)
    response=BidOrAsk.text
    response=''.join(response)#On converti la liste en string
    if(direction=='bid'):
       pos1=response.find('bids')#On trouve l'indice où est bids dans le string
       pos2=response.find('asks')-2 
       chain=response[pos1:pos2]
       print("\nThe Bids price of the asset is :\n")
    else:
        pos1=response.find('ask')
        chain=response[pos1:-2]
        print("\nThe Asks price of the asset is :\n")        
    print(chain)
    print("NB:The price is the first parameter")

def LancergetDepth():
    print("Entrez bid ou ask")
    direction=input()
    print("Entrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    getDepth(direction,pair)
    
#LancergetDepth()


#Get order book for an asset
def GetOrderBook(pair):
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/book?level=3'
    currencies = requests.get(str)
    
    print(currencies.text)
def LancerOrderBook():
    print("\nEntrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    GetOrderBook(pair)
#LancerOrderBook()
 
#create a function to read agregated trading data (candles) , ce sont les 300 dernières
def refreshDataCandle(pair,duration):
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/candles?granularity='
    str+=duration
    Candles = requests.get(str)
    print(Candles.text)

def LancerCandles():
    print("\nEntrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    print("Entrez la taille de la bougie en secondes 60, 300,900,3600,21600 ou 86400")
    duration=input()
    refreshDataCandle(pair,duration)
#LancerCandles()
#la fonction va renvoyer des données qui ont pour signification :[ time, low, high, open, close, volume ]

    
#create a sqlite table to store said data 
def CreateSqlTable():
        
    conn = sqlite3.connect('test.db')
    print ("Opened database successfully")

    conn.execute('''CREATE TABLE BTC-USD
         (ID INT PRIMARY KEY     NOT NULL,
         Exchange       TEXT    NOT NULL,
         Trading_pair   TEXT    NOT NULL,
         Duration       TEXT    NOT NULL,
         Table_name     TEXT    NOT NULL,
         Last_check     INT     NOT NULL,
         Startdate      INT     NOT NULL, 
         Last_id        INT     NOT NULL)''')
    print ("Table created successfully")
    conn.close()
#CreateSqlTable()

#function    
def CreateCandlesDB():
    
    
    print("Entrez la plateforme d'echange utilisée (Coinbase)")
    exchangeName=input()
    print("\nEntrez le couple , exemple : BTC-USD ou BTC-EUR")
    pair=input()
    print("\nEntrez la taille de la bougie en secondes 60, 300,900,3600,21600 ou 86400")
    duration=input()
    setTableName = str(exchangeName + "_" + pair + "_" + duration)
    print(setTableName)
    conn = sqlite3.connect('test9.db')
    print ("Opened database successfully")
    #l'utilisation de setTableName pour la creation de la table ne fonctionne pas , le nom est entré manuelement : Coinbase_BTC-USD_60
    conn.execute("""CREATE TABLE Coinbase_BTC-USD_60
                (Id INTEGER PRIMARY     KEY     NOT NULL,
                      date                  INT     NOT NULL,
                      high                  REAL    NOT NULL,
                      low                   REAL    NOT NULL, 
                      open                  REAL    NOT NULL, 
                      close                 REAL    NOT NULL,
                      volume                REAL    NOT NULL, 
                      quotevolume           REAL    NOT NULL, 
                      weightedaverage       REAL    NOT NULL, 
                      sma_7                 REAL    NOT NULL,
                      ema_7                 REAL    NOT NULL,
                      sma_30                REAL    NOT NULL,
                      ema_30                REAL    NOT NULL,
                      sma_200               REAL    NOT NULL,
                      ema_200               REAL    NOT NULL)""")
    
    print("Table created successfully")
    conn.close()
    
#CreateCandlesDB()


#create a function to store candle data in the db
    
#create a modify function to update when new candle data is availble








#create a function to extract all vailable trade data
def refreshData(pair):
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/trades'
    trades = requests.get(str)
    print(trades.text)

def LaunchrefreshData():
    print("\nEntrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()  
    refreshData(pair)
   
#LaunchrefreshData()
    
#create a function to store the data in sqlite
def FullDataSet():    
    print("Entrez la plateforme d'echange utilisée (Coinbase)")
    exchangeName=input()
    print("\nEntrez le couple , exemple : BTC-USD ou BTC-EUR")
    pair=input()
    
    setTableName = str(exchangeName + "_" + pair)
    
    print(setTableName)
    
    conn = sqlite3.connect('test10.db')
    print ("Opened database successfully")
   #meme probleme que pour la creation de la database precedente , la table est appellé : 
    conn.execute("""CREATE TABLE tablex
                 (Id INTEGER PRIMARY    KEY,
                 uuid                   TEXT,
                 size                   REAL,
                 price                  REAL,
                 created_at_int         INT,
                 side                   TEXT)""")
    #size = traded_btc ?
    print("Table created successfully")
    conn.close()
FullDataSet()


