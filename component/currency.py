from flask_restful import Resource
from flask import jsonify,request,send_file
from api.currency import *
class CurrencyApi(Resource):


    def get(self,yil,ay,gun):

        currency = DovizListem()

        currencyData = currency.getDovizKurListe(yil,ay,gun)
        return jsonify(currencyData)
class CurrencyUsdToEuroApi(Resource):
    def get(self,yil,ay,gun):

        currency = DovizListem()
        currencyData = currency.getCurrencyUsdToEuro(yil,ay,gun)
        return (jsonify(currencyData))
    
class CurrencyEuroToTlApi(Resource):
    def get(self,yil,ay,gun):
        currency = DovizListem()
        currencyData = currency.getCurrencyEuroToTl(yil,ay,gun)
        return (jsonify(currencyData))

class CurrencyAverageApi(Resource):
    def get(self,yil,ay,gun):
        currency = DovizListem()
        currencyData = currency.getCurrencyAverage(yil,ay,gun)
        return jsonify(currencyData)