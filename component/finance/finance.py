from flask_restful import Resource
from flask import jsonify,request,send_file
from component.finance.list import *
from component.finance.maturity import *
from component.finance.detail import *
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


class FinanceTestListFilterApi(Resource):
    def get(self):
        finance = FinanceTest()
        islem = VadeAnaliste()

        vade = islem.getVadeList()
        financeList = finance.getListFilter()
        mayaList = finance.getMayaList()
        data = {
            'financeList':financeList,
            'mayaList':mayaList,
            'vadeList':vade
            
        }
        return jsonify(data)
    

class FinanceTestListFilterMekmerAllApi(Resource):
    def get(self):
        finance = FinanceTestAll()
        islem = VadeAnaliste()

        vade = islem.getVadeList()
        financeList = finance.getListFilter()
        mayaList = finance.getMayaList()
        data = {
            'financeList':financeList,
            'mayaList':mayaList,
            'vadeList':vade
            
        }
        return jsonify(data)

class FinanceTestListFilterPoApi(Resource):
    def post(self):
        data = request.get_json()
        finance = FinanceTest()
        status = finance.setPoSaveMekmar(data)
        return {'status':status}
        
        

class FinanceTestDetailFilterApi(Resource):
    def get(self,customer):

        islem = MusteriAyrinti(customer)

        ayrinti_list = islem.getKonteynerAyrintiList()
        odeme_liste = islem.getOdemeListesi()
        po_list = islem.getByCustomersPo()
        data = {

            "ayrinti_list" : ayrinti_list,
            "odeme_liste" : odeme_liste,
            "po_list":po_list
        }


        return jsonify(data)

class FinanceTestDetailFilterMonthApi(Resource):
    def get(self,month):

        islem = MusteriAyrintiMonth()

        ayrinti_list = islem.getKonteynerAyrintiListMonth(month)

        data = {

            "ayrinti_list" : ayrinti_list,

        }


        return jsonify(data)





class FinanceTestPaidFilterApi(Resource):
    def post(self):
        data = request.get_json()
        finance = FinanceTest()
        status = finance.setPaidSave(data)
        return {'status':status}

class FinanceTestPoPaidListFilterApi(Resource):
    def get(self,po):
        finance = FinanceTest()
        liste = finance.getPoPaidList(po)
        return {'liste':liste}
    
class FinanceTestListExcelApi(Resource):
    def post(self):
        data = request.get_json()
        finance = FinanceTest()
        status = finance.getExcelList(data)
        return {'status':status}
    
    def get(self):
        
        excel_path = 'excel/dosyalar/finans_test_list.xlsx'

        return send_file(excel_path,as_attachment=True)
    
class FinanceTestListExcelApiFilter(Resource):
    def post(self):
        
        data = request.get_json()
        finance = FinanceTest()
        status = finance.getExcelListMekmerFilter(data)
        return {'status':status}
    
    def get(self):
        
        excel_path = 'excel/dosyalar/finans_test_list.xlsx'

        return send_file(excel_path,as_attachment=True)
        

    