from flask_restful import Resource
from flask import jsonify,request,send_file
from component.finance.list import *
from component.finance.maturity import *

class FinanceTestListApi(Resource):
    def get(self):
        finance = FinanceTest()
        islem = VadeAnaliste()

        vade = islem.getVadeList()
        financeList = finance.getList()
        mayaList = finance.getMayaList()
        data = {
            'financeList':financeList,
            'mayaList':mayaList,
            'vadeList':vade
            
        }
        return jsonify(data)
    
    
class FinanceTestListExcelApi(Resource):
    def post(self):
        data = request.get_json()
        finance = FinanceTest()
        status = finance.getExcelList(data)
        return {'status':status}
    
    def get(self):
        
        excel_path = 'excel/dosyalar/finans_test_list.xlsx'

        return send_file(excel_path,as_attachment=True)
        
        
    