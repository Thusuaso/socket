
from flask_restful import Resource
from flask import request,send_file,jsonify

from component.cost import *
from component.costtime import *
from component.excel import *
from component.detail import *
from component.document import *


class MaliyetRaporIslemApi(Resource):

    def get(self,yil,ay):

        islem = MaliyetRaporIslem(yil,ay)

        maliyet_listesi = islem.getMaliyetListesi()

        return maliyet_listesi
    


class MaliyetRaporIslemYilApi(Resource):
    
    def get(self,yil):

        islem = MaliyetRaporIslem_Yil(yil)

        maliyet_listesi = islem.getMaliyetListesi()

        return maliyet_listesi

class MaliyetRaporYilListApi(Resource):

    def get(self):

        islem = MaliyeZamanIslem()

        yil_listesi = islem.getYilListesi()

        return yil_listesi

class MaliyetRaporIslemAyListesi(Resource):

    def get(self,yil): 

        islem = MaliyeZamanIslem()

        ay_listesi = islem.getAyListesi(yil)

        return ay_listesi

class MaliyetRaporuAyrintiApi(Resource):

    def get(self,siparisno): 
        islem = MaliyetRaporuAyrinti()
        islem2 = EvrakListeler()
        maliyet = islem.getMaliyetAyrintiList(siparisno)

        banka = islem.getBankaAyrintiList(siparisno)

        evrak = islem2.getEvrakList(siparisno)
        
        
        data = {

            "maliyet" : maliyet,
            "banka" : banka,
            "evrak":evrak,
        }

        return jsonify(data)
               

class MaliyetRaporExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.maliyet_rapor_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/maliyet_raporlar/dosyalar/ayo_maliyet_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)
    
    
class AyoAlisFiyatiDegistirApi(Resource):
    def post(self):
        data = request.get_json()
        islem = MaliyetRaporuAyrinti()
        result = islem.setAlisFiyatiKontrolDegistir(data)
        return jsonify(result)

