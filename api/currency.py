

import urllib.request,ssl # Websitesinden veri cekmek ve ssl sertifikasini es gecmek
import xml.etree.ElementTree as ET # Xml yapisini ayristirmak
import datetime
import requests
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
from api.sql import *

class DovizListem:

    def __init__(self):

        pass

    def getDovizKurListe(self,yil,ay,gun):
        try:
            # SSl sertifikasi hatalarini engellemek
            ctx = ssl.create_default_context()

            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            x = datetime.datetime.now()
            nowDay = x.strftime('%d')
            nowMonth = x.strftime('%m')
            xy = datetime.datetime(int(yil),int(ay),int(gun))
            if(int(gun) == 29 and int(ay)==10):
                gun = 30
            if(int(gun) == int(nowDay) and int(ay) == int(nowMonth)):
                gun = int(gun) -1
            
            if (xy.strftime("%A") == "Saturday"):
                gun = str(int(gun) - 1)
                
            if len(str(gun)) == 1:
                gun = "0" + str(gun)
                
            if len(str(ay)) == 1:
                ay = "0"+ str(ay)


            
            else:
                
                if len(str(gun)) ==1:
                    gun = "0" + str(gun)
                    
                if len(str(ay)) ==1:
                    ay = "0"+ str(ay)
            
            if(int(nowDay) == int(gun) and int(ay) == int(nowMonth)):
                
                
                return
                    
            
            # URL = "https://www.tcmb.gov.tr/kurlar/202111/02112021.xml"
            URL = "https://www.tcmb.gov.tr/kurlar/"+str(yil)+str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml"

            dolar = 0
            # Websitesinden veri cekmek
            body = urllib.request.urlopen(URL,context=ctx)
            data = body.read().decode()

            # Xml dosyasini ayristirmak
            xml = ET.fromstring(data)
            for currency in xml:
                for child in currency:
                    if(child.tag == "BanknoteSelling" and currency.get("Kod") == "USD"):
                        dolar = float(child.text)
                    
                
                    else:
                        continue
            return format(dolar)
        except Exception as e:
            print("Doviz Hata",str(e))
            return 0
        

    def getCurrencyUsdToEuro (self,yil,ay,gun):
        try:
            # SSl sertifikasi hatalarini engellemek
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            x = datetime.datetime.now()
            nowDay = x.strftime('%d')
            nowMonth = x.strftime('%m')
            xy = datetime.datetime(int(yil),int(ay),int(gun))
            if(int(gun) == 29 and int(ay)==10):
                gun = 30
            if(int(gun) == int(nowDay) and int(ay) == int(nowMonth)):
                gun = int(gun) -1
            
            if (xy.strftime("%A") == "Saturday"):
                gun = str(int(gun) - 1)
                
            if len(str(gun)) == 1:
                gun = "0" + str(gun)
                
            if len(str(ay)) == 1:
                ay = "0"+ str(ay)


            
            else:
                
                if len(str(gun)) ==1:
                    gun = "0" + str(gun)
                    
                if len(str(ay)) ==1:
                    ay = "0"+ str(ay)
            
            if(int(nowDay) == int(gun) and int(ay) == int(nowMonth)):
                
                
                return
                    
            
            # URL = "https://www.tcmb.gov.tr/kurlar/202111/02112021.xml"
            URL = "https://www.tcmb.gov.tr/kurlar/"+str(yil)+str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml"

            # Websitesinden veri cekmek
            body = urllib.request.urlopen(URL,context=ctx)
            data = body.read().decode()

            # Xml dosyasini ayristirmak
            xml = ET.fromstring(data)
            dolar = 0
            euro = 0
            for currency in xml:
                for child in currency:
                    if(child.tag == "BanknoteSelling" and currency.get("Kod") == "USD"):
                        dolar = float(child.text)
                    if(child.tag == "BanknoteSelling" and currency.get("Kod") == "EUR"):
                        euro = float(child.text)
                
                    else:
                        continue
            return format(dolar/euro)
        except Exception as e:
            print("Doviz Hata",str(e))
            return 0


    def getCurrencyEuroToTl(self,yil,ay,gun):
        try:
            # SSl sertifikasi hatalarini engellemek
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            x = datetime.datetime.now()
            nowDay = x.strftime('%d')
            nowMonth = x.strftime('%m')
            xy = datetime.datetime(int(yil),int(ay),int(gun))
            if(int(gun) == 29 and int(ay)==10):
                gun = 30
            if(int(gun) == int(nowDay) and int(ay) == int(nowMonth)):
                gun = int(gun) -1
            
            if (xy.strftime("%A") == "Saturday"):
                gun = str(int(gun) - 1)
                
            if len(str(gun)) == 1:
                gun = "0" + str(gun)
                
            if len(str(ay)) == 1:
                ay = "0"+ str(ay)


            
            else:
                
                if len(str(gun)) ==1:
                    gun = "0" + str(gun)
                    
                if len(str(ay)) ==1:
                    ay = "0"+ str(ay)
            
            if(int(nowDay) == int(gun) and int(ay) == int(nowMonth)):
                
                
                return
                    
            
            # URL = "https://www.tcmb.gov.tr/kurlar/202111/02112021.xml"
            URL = "https://www.tcmb.gov.tr/kurlar/"+str(yil)+str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml"

            # Websitesinden veri cekmek
            body = urllib.request.urlopen(URL,context=ctx)
            data = body.read().decode()

            # Xml dosyasini ayristirmak
            xml = ET.fromstring(data)
            dolar = 0
            euro = 0
            for currency in xml:
                for child in currency:

                    if(child.tag == "BanknoteSelling" and currency.get("Kod") == "EUR"):
                        euro = float(child.text)
                
                    else:
                        continue
            return format(euro)
        except Exception as e:
            print("Doviz Hata",str(e))
            return 0



        
    def getDovizAvarageKurList(self,yil,ay,gun):
        try:
            # SSl sertifikasi hatalarini engellemek
            ctx = ssl.create_default_context()

            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            x = datetime.datetime.now()
            nowDay = x.strftime('%d')
            nowMonth = x.strftime('%m')
            # xy = datetime.datetime(int(yil),int(ay),int(gun))
            # if(int(gun) == 29 and int(ay)==10):
            #     gun = 30
            # if(int(gun) == int(nowDay) and int(ay) == int(nowMonth)):
            #     gun = int(gun) -1
            
            # if (xy.strftime("%A") == "Saturday"):
            #     gun = str(int(gun) - 1)
                
            # if len(str(gun)) == 1:
            #     gun = "0" + str(gun)
                
            # if len(str(ay)) == 1:
            #     ay = "0"+ str(ay)


            
            # else:
                
            if len(str(gun)) ==1:
                gun = "0" + str(gun)
                
            if len(str(ay)) == 1:
                ay = "0"+ str(ay)
            
            # if(int(nowDay) == int(gun) and int(ay) == int(nowMonth)):
                
                
            #     return
                    
            
            # URL = "https://www.tcmb.gov.tr/kurlar/202111/02112021.xml"
            URL = "https://www.tcmb.gov.tr/kurlar/"+str(yil)+str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml"
            print('URL',URL)

            dolar = 0
            # Websitesinden veri cekmek
            body = urllib.request.urlopen(URL,context=ctx)
            data = body.read().decode()

            # Xml dosyasini ayristirmak
            xml = ET.fromstring(data)
            for currency in xml:
                for child in currency:
                    if(child.tag == "BanknoteSelling" and currency.get("Kod") == "USD"):
                        dolar = float(child.text)
                    
                
                    else:
                        continue
            return format(dolar)
        except Exception as e:
            print("Doviz Hata",str(e))
            return 0
    
    def getCurrencyAverage(self,yil,ay,gun):
        total = 0
        index = 0
        for item in range(1,int(gun) + 1):
            res = self.getDovizAvarageKurList(yil,ay,item)
            if(res == 0 or res == 'Doviz Hata HTTP Error 404: Not Found'):
                continue
            else:
                total += float(res)
                index += 1
        if(total == 0):
            return 0
        else:
            sql = SqlConnect().data
            control_sql = sql.getStoreList("""
                select * from AyoCurrency where YEAR = ? and MONTH = ?
            """,(yil,ay))

            if(len(control_sql) > 0):
                            update_sql = sql.update_insert("""
                update AyoCurrency SET CURRENCY=? where YEAR=? and MONTH=?
            """,((total/index),yil,ay))
            else:
                insert_sql = sql.update_insert("""
                    insert into AyoCurrency(YEAR,MONTH,CURRENCY)
                    VALUES(?,?,?)
                """,(yil,ay,(total/index)))




            return (total/index)
        







        

        