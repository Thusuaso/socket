from flask_restful import Resource
from flask import jsonify,request,send_file
from component.excel import *
class StokRaporExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.stok_rapor_ciktisi(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'excel/dosyalar/Stok_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)   