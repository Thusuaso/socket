from flask import jsonify,request,send_file
from flask_restful import Resource
from component.excel import *
from component.mk.reports import *


class MkRaporlariExcelApi(Resource):
    def post(self):
        data = request.get_json()
        mk = ExcelCiktiIslem()
        status = mk.getMkRaporlariExcelList(data)
        return {'status':status}
    
    def get(self):

        excel_path = 'excel/dosyalar/mkRaporlari.xlsx'

        return send_file(excel_path,as_attachment=True)

class AyoCostExcelApi(Resource):

    def post(self):
        data = request.get_json()
        mk = ExcelCiktiIslem()
        status = mk.getAyoCostExcel(data)
        return {'status':status}
    
    def get(self):

        excel_path = 'excel/dosyalar/ayo_cost_excel.xlsx'

        return send_file(excel_path,as_attachment=True)
    


class MkRaporlariApi(Resource):
    def get(self,year):
        mk = MkRaporlari()
        
        byCustomerOrder = mk.getGenelMusteriSiparis()
        byPo = mk.getPoBazindaYillikSiparisler(year)
        byCustomer = mk.getMusteriBazindaUretim(year)
        byMarketing = mk.getMarketing(year)
        byMarketingYukleme = mk.getMarketingYukleme(year)
        byMarketingDetayYukleme = mk.getMarketingDetail(year)
        byYuklemevSiparisler = mk.mkRaporlarSevkSip(year)
        data = {
            'byPo':byPo,
            'byCustomer':byCustomer,
            'byMarketing':byMarketing,
            'byMarketingYukleme':byMarketingYukleme,
            'byMarketingDetayYukleme':byMarketingDetayYukleme,
            'byYuklemevSiparisler':byYuklemevSiparisler,
            'byCustomerOrder':byCustomerOrder
        }
        return jsonify(data)
