# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:42:09 2020

@author: Nicolas
"""

import requests,json,sqlite3, hmac, hashlib, time, base64

#list of all available cryptocurrencies displayed in a list
def ShowCryptoCurrencies():
    currencies = requests.get('https://api.pro.coinbase.com/products')

    r_json = json.loads(currencies.text)
    all_crypto_currencies = []
    for i in r_json:
        all_crypto_currencies.append(i['base_currency'])
    
    List_crypto_currencies=list(set(all_crypto_currencies))#this allow to remove the duplicate currencies
    List_crypto_currencies.sort()
    print(List_crypto_currencies)

#ShowCryptoCurrencies()#remove the # to test the function
    
#function to display the ask or bid price of an asset
def getDepth(direction, pair):
    
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/book'
    BidOrAsk = requests.get(str)
    response=BidOrAsk.text
    response=''.join(response)#the list is converted into a string
    if(direction=='bid'):# printing the result for bid direction
       pos1=response.find('bids')
       pos2=response.find('asks')-2 
       chain=response[pos1:pos2]
       print("\nThe Bid price of this asset is :\n")
    else:# printing the result for ask direction
        pos1=response.find('ask')
        chain=response[pos1:-2]
        print("\nThe Ask price of this asset is :\n")        
    print(chain)
    print("NB:The price is the first parameter")

def LaunchgetDepth():
    print("Entrez bid ou ask")
    direction=input()
    print("Entrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    getDepth(direction,pair)
    
#LaunchgetDepth()#remove the # to test the function


#Get order book for an asset
def GetOrderBook(pair):
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/book?level=3'
    currencies = requests.get(str)
    
    print(currencies.text)
def LaunchOrderBook():
    print("\nEntrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    GetOrderBook(pair)
#LaunchOrderBook()#remove the # to test the function
 
#create a function to read agregated trading data (candles) , the 300 last 
def refreshDataCandle(pair,duration):
    str='https://api.pro.coinbase.com/products/'
    str+=pair
    str+='/candles?granularity='
    str+=duration
    Candles = requests.get(str)
    print(Candles.text)

def LaunchCandles():
    print("\nEntrez le couple exemple : BTC-USD ou BTC-EUR")
    pair=input()
    print("Entrez la taille de la bougie en secondes 60, 300,900,3600,21600 ou 86400")
    duration=input()
    refreshDataCandle(pair,duration)
#LaunchCandles()#remove the # to test the function
#the function will return data that have the following meaning: [ time, low, high, open, close, volume ]
    
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
#CreateSqlTable()#remove the # to test the function
  
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
    #the use of setTableName for the creation of the table does not work, the name is entered manually: Coinbase_BTC-USD_60
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
    
#CreateCandlesDB()#remove the # to test the function


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
   
#LaunchrefreshData()#remove the # to test the function
    
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
  #same problem as for the creation of the previous database, the table is called :tablex
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
#FullDataSet()#remove the # to test the function





from requests.auth import AuthBase

# Create custom authentication for Exchange

class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

# Get accounts
#r = requests.get(api_url + 'accounts', auth=auth)
#print r.json()
# [{"id": "a1b2c3d4", "balance":...
    

def createOrder(api_key,secret_key,passphrase,direction,price,amount,pair='BTC-USD_d',orderType='LimitOrder'):
    api_url = 'https://api.pro.coinbase.com/'
    auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)
    order = {
        'size': amount,
        'price': price,
        'side': direction,
        'product_id': pair,
        'type':orderType,}
    r = requests.post(api_url + 'orders', json=order, auth=auth)

def cancelOrder(api_key,secret_key,uuid,passphrase):
    api_url = 'https://api.pro.coinbase.com/'
    auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase)
    r = requests.delete(api_url + 'orders'+'/'+str(uuid), auth=auth)

#apikey , secret key , passphrase a enlever avant de deposer sur git 
api_key=""
secret_key=""
passphrase=""

#createOrder(api_key,secret_key,passphrase,'buy',"0.10000000","0.01000000")#remove the # to test the function
