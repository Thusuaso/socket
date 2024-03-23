from flask import Flask,jsonify,send_file,request
from flask_restful import Api,Resource
from flask_cors import CORS,cross_origin 
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})
from openpyxl import *
import shutil

from component.main import *
from component.finance.finance import *
from component.orders.excel import *
from component.mk.mk import *
from component.stock.stock import *
class ExcellCiktiIslem:

    def ceki_listesi_excel(self,data_list):
         print(data_list)
         try:
            source_path = 'excel/sablonlar/ceki_listesi.xlsx'
            target_path = 'excel/dosyalar/ceki_listesi.xlsx'

            shutil.copy2(source_path, target_path)

            kitap = load_workbook(target_path)
            sayfa = kitap.get_sheet_by_name('Sheet')

            satir = 11
           
            for item in data_list:

                sayfa.cell(satir,column=2,value=item['KasaNo'])
                sayfa.cell(satir,column=3,value=item['KategoriAdi'])
                sayfa.cell(satir,column=4,value=item['YuzeyIslem'])
                sayfa.cell(satir,column=5,value=item['UrunAdi'])
                sayfa.cell(satir,column=6,value=item['Kenar'])
                sayfa.cell(satir,column=7,value=item['En'])
                sayfa.cell(satir,column=8,value=item['Boy'])
                sayfa.cell(satir,column=9,value=item['KutuAdet'])
                sayfa.cell(satir,column=10,value=item['Adet'])

                miktar = 0
                kutu = int(item['KutuAdet'])
                if(item['BirimAdi'] == 'M2'):
                    
                    if(item['En']=='ANT' and item['Boy']=='PAT'):
                        miktar = float(round((0.74338688 * kutu),2))
                        
                    elif(item['En']=='20,3' and item['Boy']=='SET'):
                        miktar=float(round((0.494914 * kutu),2))
                    elif(item['En'] == 'VAR') or (item['En'] == 'Various') or (item['En'] == '1 LT'):
                        miktar = float(item['Miktar'])
                    else:
                        miktar = float(item['Miktar'])
                elif (item['BirimAdi'] == 'Adet'):
                    if(float(item['Miktar']) != None or float(item['Miktar']) != 0):
                        
                        miktar = float(item['Miktar'])
                    else:
                        miktar = '-'
                elif (item['BirimAdi'] == 'Mt'):
                    miktar=float(item['Miktar'])
                sayfa.cell(satir,column=11,value=miktar)
                kg = 0
                
                if(item['Kenar']):
                    if (item['Kenar']=='VAR') or (item['Kenar'] == 'Various') or (item['Kenar'] == 'Other' or (item['Kenar'] == '1 LT')):
                        kenar = 1
                    else: 
                        kenar = item['Kenar'].replace(',','.')
                        kenar = float(kenar)
                
                else:
                    kenar=1
                if (item['BirimAdi'] == 'M2'):
                    if (item['KategoriAdi'] == 'Travertine Tiles'):
                        kg = int(round((kenar * miktar * 10.0 * 2.40),0))
                    elif (item['KategoriAdi'] == 'Marble Tiles'):
                        kg = int(round((kenar * miktar * 10.0 * 2.80),0))
                    elif (item['KategoriAdi'] == 'Other'):
                        kg = int(round((kenar * miktar * 10 * 1),0))
                    elif ((item['KategoriAdi'] == 'Travertine Mosaic') and (item['YuzeyIslem'] == 'Split face')):
                        kg = int(round((1.5 * miktar * 10 * 2.40),0))
                    else:
                        kg=0
                    
                    
                sayfa.cell(satir,column=12,value=item['Ton'])
                sayfa.cell(satir,column=13,value=float(item['Ton']) + 30)
                
                
                
                satir += 1
          
            kitap.save(target_path)
            kitap.close()

            return True

         except Exception as e:
            print('ceki_listesi_excel  Hata : ',str(e))
            return False  
        
   
class SiparisCekiListesiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcellCiktiIslem()

        result = islem.ceki_listesi_excel(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'excel/dosyalar/ceki_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)
    
   
api.add_resource(SiparisCekiListesiApi, '/excel/check/list', methods=['GET','POST'])
api.add_resource(MaliyetRaporIslemApi,'/maliyet/listeler/maliyetListesi/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(MaliyetRaporIslemYilApi,'/maliyet/listeler/maliyetListesi/<int:yil>',methods=['GET'])
api.add_resource(FinanceTestListApi,'/finance/reports/test',methods=['GET'])
api.add_resource(FinanceTestListExcelApi,'/finance/reports/test/excel',methods=['GET','POST'])
api.add_resource(UretimExcelCiktiApi,'/siparisler/dosyalar/uretimExcelCikti',methods=['POST','GET'])
api.add_resource(MkRaporlariExcelApi,'/raporlar/listeler/mkraporlari/excel',methods=['GET','POST'])
api.add_resource(MkRaporlariApi,'/raporlar/listeler/mkraporlari/<int:year>',methods=['GET'])
api.add_resource(StokRaporExcelApi,'/raporlar/listeler/stokRaporExcelListe',methods=['GET','POST'])
api.add_resource(MaliyetRaporExcelApi, '/maliyet/dosyalar/maliyetRaporExcelListe', methods=['GET','POST'])




 

if __name__ == '__main__':
    app.run(port=5000,debug=True)