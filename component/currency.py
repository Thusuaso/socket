from flask_restful import Resource
from flask import jsonify,request,send_file
from api.currency import *
class CurrencyApi(Resource):


    def get(self,yil,ay,gun):

        currency = DovizListem()

        currencyData = currency.getDovizKurListe(yil,ay,gun)
        return jsonify(currencyData)