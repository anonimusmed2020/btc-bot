import time
import pandas as pd
from ta import *
import csv
import os
import sqlite3
from sqlite3 import Error
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from binance.client import Client
import mysql.connector as mariadb
#mariadb_connection = mariadb.connect(user='admin_bot', password='BE5zXImvh-7zi3bKOmxp', database='data')
#cursor = mariadb_connection.cursor()

mariadb_connection = mariadb.connect(user='crypdxzp_datauser', password='BE5zXImvh-7zi3bKOmxp', database='crypdxzp_data', host='127.0.0.1', port='3306')
cursor = mariadb_connection.cursor()
prices = []

tradePlaced = False
typeOfTrade = False

api_key = 'aqui va la api_ key'
api_secret = 'aqui va la api_secret' 


client = Client(api_key,api_secret)

def promedio(valores):
        sumaParcial=0
        for valor in valores:
                sumaParcial+=float(valor)
        cantidadValores = len(valores)
        return sumaParcial/float(cantidadValores)
        
def clear():
    os.system('clear')
    return

if __name__ == "__main__":
    while True:
        info = client.get_klines(symbol = 'BTCUSDT', limit=1,interval=Client.KLINE_INTERVAL_1MINUTE)
        infoticker = client.get_ticker(symbol = 'BTCUSDT')
        lasticker_price = float(infoticker["lastPrice"])
        info_limit1 = info[0]
            
        open_btc = float(info_limit1[1])
        high_btc = float(info_limit1[2])
        low_btc = float(info_limit1[3])
        close_btc = float(info_limit1[4])
        volume_btc = float(info_limit1[5])
        
        cursor.execute("INSERT INTO tickers_btc (open,high,low,close,volume) VALUES (%s,%s,%s,%s,%s)", (open_btc, high_btc, low_btc, close_btc, volume_btc))
        mariadb_connection.commit()
        
        query = "SELECT * FROM tickers_btc;"
        
        df  = pd.read_sql_query(query,mariadb_connection)
        
        df = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df1 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df2 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df3 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df4 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df5 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df6 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df7 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        df8 = add_all_ta_features(df, 'open', 'high', 'low', 'close', 'volume', fillna = True)
        
        print(df.columns)
        df = df.trend_ema_fast
        df1 = df1.trend_macd_diff
        df2 = df2.volume_obv
        df3 = df3.volume_vpt
        df4 = df4.trend_ema_slow
        df5 = df5.volatility_bbh
        df6 = df6.volatility_bbl
        df7 = df7.volatility_bbm
        df8 = df8.momentum_rsi
        
        last20emafast = df[-20:]
        last200emaslow = df4[-200:]
        last50macd_diff = df1[-50:]
        last200volOBV = df2[-200:]
        last200volVPT = df3[-200:]
        last200bolhigh = df5[-8:]
        last200bollow = df6[-8:]
        last200bolma = df7[-8:]
        lastrsi = df8[-8:]
        
        ema_20= promedio(last20emafast)
        ema_200= promedio(last200emaslow)
        emacd_50= promedio(last50macd_diff)
        volobv_200= promedio(last200volOBV)
        volvpt_200= promedio(last200volVPT)
        bolhigh_200= promedio(last200bolhigh)
        bollow_200= promedio(last200bollow)
        bolma_200= promedio(last200bolma)
        rsi= promedio(lastrsi)
        
        #colo = int(len(df)) - 1
        #colo1 = int(len(df1)) - 1
        #colo2 = int(len(df2)) - 1
        #colo3 = int(len(df3)) - 1
        #colo4 = int(len(df4)) - 1
        
        #ema_fast = df.iloc[colo]
        #emac_diff = df1.iloc[colo1]
        #vol_obv= df2.iloc[colo2]
        #vol_fi= df3.iloc[colo3]
        #ema_slow = df4.iloc[colo4]
        #print(lasticker_price)
        #print(typeOfTrade)
        #print(prices)
        print(rsi)
        print('---------------------BTC ANALYSIS - CRYPTXEL IA BOT-----------------------')
        print('Open ==>  ' + '%.2f' % open_btc)
        print ('High ==>  ' + '%.2f' % high_btc)
        print('Low ==>  ' + '%.2f' %low_btc)
        print ('Close ==> ' + '%.2f' %close_btc)
        print('Volume ==>  ' + '%.2f' %volume_btc)
        print('Last Price ==>  ' + '%.2f' %lasticker_price)
        
        print('--------------------------------------------')
        print('Indicadores de Tendencias')
        print('--------------------------------------------')
        print (' Slow EMA :' + '%.2f' % ema_200 + ' Fast EMA :' + '%.2f' % ema_20 + ' EMAC_diff :' + '%.2f' % emacd_50)
        print('Indicadores de Volatilidad')
        print('--------------------------------------------')
        print ('Bollinger High :' + '%.2f' % bolhigh_200 + 'Bollinger ma :' + '%.2f' % bolma_200 + ' Bollinger Low :' + '%.2f' % bollow_200)
        print('Indicadores de Volumen')
        print('--------------------------------------------')
        print ('Vol OBV:' + '%.2f' % volobv_200 + ' Vol VPT :' + '%.2f' % volvpt_200)
        
        
        
        
        
        data = 0
        cursor.execute("""UPDATE ia_data_res SET ema_fast = %s , ema_slow = %s, emac_diff = %s , bbHigh = %s , bbMid = %s , bbLow = %s , vol_obv = %s , vol_vpt = %s, LastPrice = %s WHERE id = %s""",(float(ema_20), float(ema_200), float(emacd_50), float(bolhigh_200), float(bolma_200), float(bollow_200), float(volobv_200), float(volvpt_200), float(lasticker_price), data))
        mariadb_connection.commit()
        
        #if (len(prices) > 0):
                
                #previousPrice = prices[-1]
                #if (not tradePlaced):
                                #if ( (lasticker_price > ema_200) and (lasticker_price < previousPrice) ):
					#print "SELL ORDER"
					##orderNumber = conn.sell(pair,lastPairPrice,.01)
					#tradePlaced = True
					#typeOfTrade = "short"
                                        #cursor.execute("INSERT INTO ia_data_orders (order_id,order_type,order_price,order_quan,order_status,order_profit) VALUES (%s,%s,%s,%s,%s,%s)", (1890, "SELL", bolhigh_200, 0.01, "OPEN",1))
                                        #mariadb_connection.commit()
                                        ##order = client.create_order(symbol='BTCUSDT',side=SIDE_SELL,type=ORDER_TYPE_LIMIT,timeInForce=TIME_IN_FORCE_GTC,quantity=100,price='0.00001')
                                #elif ( (lasticker_price < ema_200) and (lasticker_price > previousPrice) ):
					#print "BUY ORDER"
					##orderNumber = conn.buy(pair,lastPairPrice,.01)
					#tradePlaced = True
					#typeOfTrade = "long"
                                        #cursor.execute("INSERT INTO ia_data_orders (order_id,order_type,order_price,order_quan,order_status,order_profit) VALUES (%s,%s,%s,%s,%s,%s)", (1890, "BUY", bollow_200, 0.01, "OPEN",1))
                                        #mariadb_connection.commit()
                                        ##order = client.create_order(symbol='BTCUSDT',side=SIDE_BUY,type=ORDER_TYPE_LIMIT,timeInForce=TIME_IN_FORCE_GTC,quantity=100,price='0.00001')

                #elif (typeOfTrade == "short"):
                                #print "We are in short alert"
                                #if ( lasticker_price > bolhigh_200 ):
					#print "EXIT TRADE"
					##conn.cancel(pair,orderNumber)
					#tradePlaced = False
					#typeOfTrade = False
                                        #order_id = 1890
                                        #order_status = "OPEN"
                                        #cursor.execute("""UPDATE ia_data_orders SET order_status = %s, order_profit = %s WHERE order_id = %s , order_status = %s""",( "CLOSE", 0, order_id, order_status))
                                        #mariadb_connection.commit()
                #elif (typeOfTrade == "long"):
                                #print "We are in long alert"
                                #if ( lasticker_price < bollow_200 ):
					#print "EXIT TRADE"
					##conn.cancel(pair,orderNumber)
					#tradePlaced = False
					#typeOfTrade = False
        #else:
			#previousPrice = 0
        
        #prices.append(float(lasticker_price))
        
        time.sleep(0.1)
        clear()
		
