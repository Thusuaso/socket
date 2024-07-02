from flask import Flask,jsonify,send_file,request
from flask_restful import Api,Resource
from flask_cors import CORS,cross_origin 
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})
from openpyxl import *
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font,Alignment
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText
import shutil

from component.main import *
from component.finance.finance import *
from component.orders.excel import *
from component.mk.mk import *
from component.stock.stock import *
from component.currency import *
class ExcellCiktiIslem:

    def ceki_listesi_excel(self,data_list):
         try:
            source_path = 'excel/sablonlar/ceki_listesi.xlsx'
            target_path = 'excel/dosyalar/ceki_listesi.xlsx'

            shutil.copy2(source_path, target_path)

            kitap = load_workbook(target_path)
            sayfa = kitap['Sheet']

            satir = 11
            index = 1
            total_m2 = 0
            total_piece = 0
            total_mt = 0
            total_ton_1 = 0
            total_ton_2 = 0
            thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
            font = Font(name='Calibri',
                size=11,
                bold=True,
                italic=False,
                vertAlign=None,
                underline='none',
                strike=False,
                color='FF000000')
            po = data_list['po']
            sayfa.cell(6,column=1,value= po + ' Packing List')
            for item in data_list['list']:
                sayfa.cell(satir,column=1,value=index).border = thin_border
                sayfa.cell(satir,column=2,value=item['KasaNo']).border = thin_border
                sayfa.cell(satir,column=3,value=item['KategoriAdi']).border = thin_border
                sayfa.cell(satir,column=4,value=item['YuzeyIslem']).border = thin_border
                sayfa.cell(satir,column=5,value=item['UrunAdi']).border = thin_border
                sayfa.cell(satir,column=6,value=item['Kenar']).border = thin_border
                sayfa.cell(satir,column=7,value=item['En']).border = thin_border
                sayfa.cell(satir,column=8,value=item['Boy']).border = thin_border
                sayfa.cell(satir,column=9,value=item['KutuAdet']).border = thin_border
                sayfa.cell(satir,column=10,value=item['Adet']).border = thin_border

                miktar = 0
                kutu = int(item['KutuAdet'])
                if(item['BirimAdi'] == 'Sqm'):
                    if(item['En']=='ANT' and item['Boy']=='PAT'):
                        miktar = float(round((0.74338688 * kutu),2))
                        
                    elif(item['En']=='20,3' and item['Boy']=='SET'):
                        miktar=float(round((0.494914 * kutu),2))
                    elif(item['En'] == 'VAR') or (item['En'] == 'Various') or (item['En'] == '1 LT'):
                        miktar = float(item['Miktar'])
                    else:
                        miktar = float(item['Miktar'])
                elif (item['BirimAdi'] == 'Pcs'):
                    
                    if(float(item['Miktar']) != None or float(item['Miktar']) != 0):
                        
                        miktar = float(item['Miktar'])
                    else:
                        miktar = '-'
                elif (item['BirimAdi'] == 'Mt'):
                    miktar=float(item['Miktar'])

                if(item['BirimAdi'] == 'Sqm'):
                    total_m2 += miktar
                    sayfa.cell(satir,column=11,value=miktar).border = thin_border
                else:
                    sayfa.cell(satir,column=11,value="").border = thin_border

                if(item['BirimAdi'] == 'Pcs'):
                    total_piece += miktar
                    sayfa.cell(satir,column=12,value=miktar).border = thin_border
                else:
                    sayfa.cell(satir,column=12,value="").border = thin_border
                if(item['BirimAdi'] == 'Mt'):
                    total_mt += miktar
                    sayfa.cell(satir,column=13,value=miktar).border = thin_border
                else:
                    sayfa.cell(satir,column=13,value="").border = thin_border

                
                if(item['Ton'] == None or item['Ton'] == 'None' or item['Ton'] == 'undefined'):
                    sayfa.cell(satir,column=14,value=0).border = thin_border
                    sayfa.cell(satir,column=15,value = 0).border = thin_border
                else:
                    total_ton_1 += int(item['Ton'])
                    total_ton_2 += int(item['Ton']) + 30
                    sayfa.cell(satir,column=14,value=int(item['Ton'])).border = thin_border
                    sayfa.cell(satir,column=15,value=int(item['Ton']) + 30).border = thin_border
                
                
                
                satir += 1
                index += 1

            m2font = sayfa.cell(satir,column=11,value=total_m2)
            piecefont =sayfa.cell(satir,column=12,value=total_piece)
            mtfont =sayfa.cell(satir,column=13,value=total_mt)
            ton1font =sayfa.cell(satir,column=14,value=int(total_ton_1))
            ton2font =sayfa.cell(satir,column=15,value=int(total_ton_2))
            m2font.font = font
            piecefont.font = font
            mtfont.font = font
            ton1font.font = font
            ton2font.font = font
            m2font.border = thin_border
            piecefont.border = thin_border
            mtfont.border = thin_border
            ton1font.border = thin_border
            ton2font.border = thin_border

            satir += 2
            merge_1 = 'A' + str(satir) + ':' + 'B' + str(satir)
            sayfa.merge_cells(merge_1)
            total_cases = sayfa.cell(satir,column=1,value="TOTAL CASES")
            sayfa.cell(satir,column=2).border = thin_border
            total_cases.border = thin_border
            total_cases.font = font
            total_cases.alignment  = Alignment(horizontal="center", vertical="center")
            merge_2 = 'C' + str(satir) + ':' + 'D' + str(satir)
            sayfa.merge_cells(merge_2)
            case_total = sayfa.cell(satir,column = 3,value=str(index -1) + ' ' + 'W.CASES')
            sayfa.cell(satir,column=4).border = thin_border
            case_total.border = thin_border
            case_total.font = font
            case_total.alignment  = Alignment(horizontal="center", vertical="center")

            satir += 2

            merge_3 = 'A' + str(satir) + ':' + 'B' + str(satir)
            sayfa.merge_cells(merge_3)
            total_ton = sayfa.cell(satir,column=1,value="TOTAL NET KG")
            sayfa.cell(satir,column=2).border = thin_border
            total_ton.border = thin_border
            total_ton.font = font
            total_ton.alignment  = Alignment(horizontal="center", vertical="center")

            merge_4 = 'C' + str(satir) + ':' + 'D' + str(satir)
            sayfa.merge_cells(merge_4)
            sum_ton = sayfa.cell(satir,column = 3,value=str(total_ton_1) + ' ' + 'kgs')
            sayfa.cell(satir,column=4).border = thin_border
            sum_ton.border = thin_border
            sum_ton.font = font
            sum_ton.alignment  = Alignment(horizontal="center", vertical="center")


            satir += 2

            merge_5 = 'A' + str(satir) + ':' + 'B' + str(satir)
            sayfa.merge_cells(merge_5)
            total_ton_gross = sayfa.cell(satir,column=1,value="TOTAL GROSS KG ")
            sayfa.cell(satir,column=2).border = thin_border
            total_ton_gross.border = thin_border
            total_ton_gross.font = font
            total_ton_gross.alignment  = Alignment(horizontal="center", vertical="center")

            merge_6 = 'C' + str(satir) + ':' + 'D' + str(satir)
            sayfa.merge_cells(merge_6)
            sum_gross_ton = sayfa.cell(satir,column = 3,value=str(total_ton_2) + ' ' + 'kgs')
            sayfa.cell(satir,column=4).border = thin_border
            sum_gross_ton.border = thin_border
            sum_gross_ton.font = font
            sum_gross_ton.alignment  = Alignment(horizontal="center", vertical="center")

            satir += 2

            merge_7 = 'A' + str(satir) + ':' +'D' + str(satir)
            sayfa.merge_cells(merge_7)
            description = sayfa.cell(satir,column = 1,value="EK AÇIKLAMALAR")
            sayfa.cell(satir,column=2).border = thin_border
            sayfa.cell(satir,column=3).border = thin_border
            sayfa.cell(satir,column=4).border = thin_border


            description.border = thin_border
            description.font = font
            description.alignment  = Alignment(horizontal="center", vertical="center")


            merge_8 = 'A' + str(satir + 1) + ':' +'D' + str(satir + 3)
            sayfa.merge_cells(merge_8)
            sayfa.cell(satir + 1,column=1).border = thin_border
            sayfa.cell(satir + 1,column=2).border = thin_border
            sayfa.cell(satir + 1,column=3).border = thin_border
            sayfa.cell(satir + 1,column=4).border = thin_border

            sayfa.cell(satir + 2,column=1).border = thin_border
            sayfa.cell(satir + 2,column=2).border = thin_border
            sayfa.cell(satir + 2,column=3).border = thin_border
            sayfa.cell(satir + 2,column=4).border = thin_border

            sayfa.cell(satir + 3,column=1).border = thin_border
            sayfa.cell(satir + 3,column=2).border = thin_border
            sayfa.cell(satir + 3,column=3).border = thin_border
            sayfa.cell(satir + 3,column=4).border = thin_border





            merge_8 = 'E' + str(satir) + ':' +'O' + str(satir)
            sayfa.merge_cells(merge_8)
            crates_size = sayfa.cell(satir,column = 5,value="KASA ÖLÇÜLERİ")
            sayfa.cell(satir,column=5).border = thin_border
            sayfa.cell(satir,column=6).border = thin_border
            sayfa.cell(satir,column=7).border = thin_border
            sayfa.cell(satir,column=8).border = thin_border
            sayfa.cell(satir,column=9).border = thin_border
            sayfa.cell(satir,column=10).border = thin_border
            sayfa.cell(satir,column=11).border = thin_border
            sayfa.cell(satir,column=12).border = thin_border
            sayfa.cell(satir,column=13).border = thin_border
            sayfa.cell(satir,column=14).border = thin_border
            sayfa.cell(satir,column=15).border = thin_border



            crates_size.border = thin_border
            crates_size.font = font
            crates_size.alignment  = Alignment(horizontal="center", vertical="center")


            merge_9 = 'E' + str(satir + 1) + ':' +'O' + str(satir + 3)
            sayfa.merge_cells(merge_9)
            sayfa.cell(satir + 1,column=5).border = thin_border
            sayfa.cell(satir + 1,column=6).border = thin_border
            sayfa.cell(satir + 1,column=7).border = thin_border
            sayfa.cell(satir + 1,column=8).border = thin_border
            sayfa.cell(satir + 1,column=9).border = thin_border
            sayfa.cell(satir + 1,column=10).border = thin_border
            sayfa.cell(satir + 1,column=11).border = thin_border
            sayfa.cell(satir + 1,column=12).border = thin_border
            sayfa.cell(satir + 1,column=13).border = thin_border
            sayfa.cell(satir + 1,column=14).border = thin_border
            sayfa.cell(satir + 1,column=15).border = thin_border



            sayfa.cell(satir + 2,column=5).border = thin_border
            sayfa.cell(satir + 2,column=6).border = thin_border
            sayfa.cell(satir + 2,column=7).border = thin_border
            sayfa.cell(satir + 2,column=8).border = thin_border
            sayfa.cell(satir + 2,column=9).border = thin_border
            sayfa.cell(satir + 2,column=10).border = thin_border
            sayfa.cell(satir + 2,column=11).border = thin_border
            sayfa.cell(satir + 2,column=12).border = thin_border
            sayfa.cell(satir + 2,column=13).border = thin_border
            sayfa.cell(satir + 2,column=14).border = thin_border
            sayfa.cell(satir + 2,column=15).border = thin_border

            sayfa.cell(satir + 3,column=5).border = thin_border
            sayfa.cell(satir + 3,column=6).border = thin_border
            sayfa.cell(satir + 3,column=7).border = thin_border
            sayfa.cell(satir + 3,column=8).border = thin_border
            sayfa.cell(satir + 3,column=9).border = thin_border
            sayfa.cell(satir + 3,column=10).border = thin_border
            sayfa.cell(satir + 3,column=11).border = thin_border
            sayfa.cell(satir + 3,column=12).border = thin_border
            sayfa.cell(satir + 3,column=13).border = thin_border
            sayfa.cell(satir + 3,column=14).border = thin_border
            sayfa.cell(satir + 3,column=15).border = thin_border

            satir += 5
            merge_10 = 'A' + str(satir) + ':' +'D' + str(satir)
            sayfa.merge_cells(merge_10)
            container = sayfa.cell(satir,column = 1,value="KONTEYNER İÇİ DAĞILIM")
            sayfa.cell(satir,column=2).border = thin_border
            sayfa.cell(satir,column=3).border = thin_border
            sayfa.cell(satir,column=4).border = thin_border


            container.border = thin_border
            container.font = font
            container.alignment  = Alignment(horizontal="center", vertical="center")


            merge_11 = 'A' + str(satir + 1) + ':' +'D' + str(satir + 3)
            sayfa.merge_cells(merge_11)
            sayfa.cell(satir + 1,column=1).border = thin_border
            sayfa.cell(satir + 1,column=2).border = thin_border
            sayfa.cell(satir + 1,column=3).border = thin_border
            sayfa.cell(satir + 1,column=4).border = thin_border

            sayfa.cell(satir + 2,column=1).border = thin_border
            sayfa.cell(satir + 2,column=2).border = thin_border
            sayfa.cell(satir + 2,column=3).border = thin_border
            sayfa.cell(satir + 2,column=4).border = thin_border

            sayfa.cell(satir + 3,column=1).border = thin_border
            sayfa.cell(satir + 3,column=2).border = thin_border
            sayfa.cell(satir + 3,column=3).border = thin_border
            sayfa.cell(satir + 3,column=4).border = thin_border




            merge_12 = 'E' + str(satir) + ':' +'O' + str(satir)
            sayfa.merge_cells(merge_12)
            notes = sayfa.cell(satir,column = 5,value="YÜKLEME TOPLANTISI NOTLARI")
            sayfa.cell(satir,column=5).border = thin_border
            sayfa.cell(satir,column=6).border = thin_border
            sayfa.cell(satir,column=7).border = thin_border
            sayfa.cell(satir,column=8).border = thin_border
            sayfa.cell(satir,column=9).border = thin_border
            sayfa.cell(satir,column=10).border = thin_border
            sayfa.cell(satir,column=11).border = thin_border
            sayfa.cell(satir,column=12).border = thin_border
            sayfa.cell(satir,column=13).border = thin_border
            sayfa.cell(satir,column=14).border = thin_border
            sayfa.cell(satir,column=15).border = thin_border



            notes.border = thin_border
            notes.font = font
            notes.alignment  = Alignment(horizontal="center", vertical="center")


            merge_13 = 'E' + str(satir + 1) + ':' +'O' + str(satir + 3)
            sayfa.merge_cells(merge_13)
            sayfa.cell(satir + 1,column=5).border = thin_border
            sayfa.cell(satir + 1,column=6).border = thin_border
            sayfa.cell(satir + 1,column=7).border = thin_border
            sayfa.cell(satir + 1,column=8).border = thin_border
            sayfa.cell(satir + 1,column=9).border = thin_border
            sayfa.cell(satir + 1,column=10).border = thin_border
            sayfa.cell(satir + 1,column=11).border = thin_border
            sayfa.cell(satir + 1,column=12).border = thin_border
            sayfa.cell(satir + 1,column=13).border = thin_border
            sayfa.cell(satir + 1,column=14).border = thin_border
            sayfa.cell(satir + 1,column=15).border = thin_border



            sayfa.cell(satir + 2,column=5).border = thin_border
            sayfa.cell(satir + 2,column=6).border = thin_border
            sayfa.cell(satir + 2,column=7).border = thin_border
            sayfa.cell(satir + 2,column=8).border = thin_border
            sayfa.cell(satir + 2,column=9).border = thin_border
            sayfa.cell(satir + 2,column=10).border = thin_border
            sayfa.cell(satir + 2,column=11).border = thin_border
            sayfa.cell(satir + 2,column=12).border = thin_border
            sayfa.cell(satir + 2,column=13).border = thin_border
            sayfa.cell(satir + 2,column=14).border = thin_border
            sayfa.cell(satir + 2,column=15).border = thin_border

            sayfa.cell(satir + 3,column=5).border = thin_border
            sayfa.cell(satir + 3,column=6).border = thin_border
            sayfa.cell(satir + 3,column=7).border = thin_border
            sayfa.cell(satir + 3,column=8).border = thin_border
            sayfa.cell(satir + 3,column=9).border = thin_border
            sayfa.cell(satir + 3,column=10).border = thin_border
            sayfa.cell(satir + 3,column=11).border = thin_border
            sayfa.cell(satir + 3,column=12).border = thin_border
            sayfa.cell(satir + 3,column=13).border = thin_border
            sayfa.cell(satir + 3,column=14).border = thin_border
            sayfa.cell(satir + 3,column=15).border = thin_border







  






















            kitap.save(target_path)
            kitap.close()

            return True

         except Exception as e:
            print('ceki_listesi_excel  Hata : ',str(e))
            return False  
    
    def seleksiyon_listesi_excel(self,data_list):
        try:
        
            source_path = 'excel/sablonlar/seleksiyon_etiket.xlsx'
            target_path = 'excel/dosyalar/seleksiyon_etiket.xlsx'

            shutil.copy2(source_path, target_path)

            kitap = load_workbook(target_path)
            sayfa = kitap['Sheet']
            satir = 1
            column = 1
            thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
            for i in data_list:
 

                case_no = sayfa.cell(satir,column=column,value='CASE NO:')
                case_no.border = thin_border
                case_no.font = Font(bold=True)
                case_no.alignment = Alignment(horizontal="center", vertical="center")
                case_merge = 'B' + str(satir) + ':' + 'D' + str(satir)
                sayfa.merge_cells(case_merge)
                case = sayfa.cell(satir,column=column + 1,value=i['KasaNo'])
                sayfa.cell(satir,column=column + 2).border = thin_border
                sayfa.cell(satir,column=column + 3).border = thin_border
                case.border = thin_border
                case.alignment = Alignment(horizontal="center", vertical="center")
                case.font = Font(size=20,bold=True)

                status = sayfa.cell(satir + 1,column=column,value='STATUS: ')
                status.border = thin_border
                status.alignment = Alignment(horizontal="center", vertical="center")
                status.font = Font(bold=True)
                status_merge = 'B' + str(satir + 1) + ':' + 'D' + str(satir + 1)
                sayfa.merge_cells(status_merge)

                stock = sayfa.cell(satir + 1,column=column + 1,value='STOK')
                sayfa.cell(satir+1,column=column + 2).border = thin_border
                sayfa.cell(satir+1,column=column + 3).border = thin_border
                stock.border = thin_border
                stock.alignment = Alignment(horizontal="center", vertical="center")
                stock.font = Font(size=20,bold=True)

                destination = sayfa.cell(satir,column = column + 4,value = 'DESTINATION')
                destination.border = thin_border
                destination.alignment = Alignment(horizontal="center", vertical="center")
                destination.font = Font(bold=True)
                country = sayfa.cell(satir + 1,column = column + 4,value = 'TR')
                country.border = thin_border
                country.alignment = Alignment(horizontal="center", vertical="center")
                country.font = Font(size=14,bold=True)

                product_name = i['KategoriAdi'] + ' / ' + i['UrunAdi'] + ' / ' + i['YuzeyIslemAdi'] + ' / ' + str(i['En']) + 'x' + str(i['Boy']) + 'x' +  str(i['Kenar']) + ' / ' + str(i['Adet']) + ' pcs / ' + str(i['Miktar']) + ' ' + i['UrunBirimAdi']
                product_merge = 'A' + str(satir + 2) + ':' + 'E' + str(satir + 7)
                sayfa.merge_cells(product_merge)
                product = sayfa.cell(satir + 2,column = column,value=product_name)
                product.border = thin_border
                product.alignment = Alignment(horizontal="center", vertical="center",wrapText=True)
                product.font = Font(size=24,bold=True)
                sayfa.cell(satir + 2,column = column).border = thin_border
                sayfa.cell(satir + 3,column = column).border = thin_border
                sayfa.cell(satir + 4,column = column).border = thin_border
                sayfa.cell(satir + 5,column = column).border = thin_border
                sayfa.cell(satir + 6,column = column).border = thin_border
                sayfa.cell(satir + 7,column = column).border = thin_border

                sayfa.cell(satir + 2,column = column+4).border = thin_border
                sayfa.cell(satir + 3,column = column+4).border = thin_border
                sayfa.cell(satir + 4,column = column+4).border = thin_border
                sayfa.cell(satir + 5,column = column+4).border = thin_border
                sayfa.cell(satir + 6,column = column+4).border = thin_border
                sayfa.cell(satir + 7,column = column+4).border = thin_border

                sayfa.cell(satir + 7,column = column+1).border = thin_border
                sayfa.cell(satir + 7,column = column+2).border = thin_border
                sayfa.cell(satir + 7,column = column+3).border = thin_border

                satir += 9


            kitap.save(target_path)
            kitap.close()
            return True

                

                

        except Exception as e:
            print('seleksiyon etiket çıktı hata',str(e))
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
    
class SeleksiyonUrunEtiketApi(Resource):
    def post(self):
        data = request.get_json()
        excel = ExcellCiktiIslem()
        status = excel.seleksiyon_listesi_excel(data)
        return jsonify({'status':status})
    
    def get(self):

        excel_path = 'excel/dosyalar/seleksiyon_etiket.xlsx'

        return send_file(excel_path,as_attachment=True)


   
api.add_resource(SiparisCekiListesiApi, '/excel/check/list', methods=['GET','POST'])
api.add_resource(MaliyetRaporIslemApi,'/maliyet/listeler/maliyetListesi/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(MaliyetRaporIslemYilApi,'/maliyet/listeler/maliyetListesi/<int:yil>',methods=['GET'])
api.add_resource(FinanceTestListApi,'/finance/reports/test',methods=['GET'])
api.add_resource(FinanceTestListExcelApi,'/finance/reports/test/excel',methods=['GET','POST'])
api.add_resource(FinanceTestListExcelApiFilter,'/finance/reports/test/excel/mekmer',methods=['GET','POST'])

api.add_resource(UretimExcelCiktiApi,'/siparisler/dosyalar/uretimExcelCikti',methods=['POST','GET'])
api.add_resource(MkRaporlariExcelApi,'/raporlar/listeler/mkraporlari/excel',methods=['GET','POST'])
api.add_resource(MkRaporlariApi,'/raporlar/listeler/mkraporlari/<int:year>',methods=['GET'])
api.add_resource(StokRaporExcelApi,'/raporlar/listeler/stokRaporExcelListe',methods=['GET','POST'])
api.add_resource(MaliyetRaporExcelApi, '/maliyet/dosyalar/maliyetRaporExcelListe', methods=['GET','POST'])
api.add_resource(CurrencyApi,'/finance/doviz/liste/<string:yil>/<string:ay>/<string:gun>',methods=['GET'])

api.add_resource(FinanceTestListFilterApi,'/finance/reports/test/filter',methods=['GET'])
api.add_resource(FinanceTestDetailFilterApi,'/finance/po/list/mekmer/<int:customer>',methods=['GET'])

api.add_resource(FinanceTestDetailFilterMonthApi,'/finance/po/list/mekmer/month/<int:month>',methods=['GET'])



api.add_resource(FinanceTestPaidFilterApi,'/finance/po/paid/mekmer/save',methods=['POST'])
api.add_resource(FinanceTestPoPaidListFilterApi,'/finance/po/paid/list/mekmer/<string:po>',methods=['GET'])

api.add_resource(FinanceTestListFilterMekmerAllApi,'/finance/reports/mekmer/all',methods=['GET'])

api.add_resource(FinanceTestListFilterPoApi,'/finance/mekmar/po/paid/save',methods=['POST'])



api.add_resource(GuReportsSellerAndOperationOrdersExcelApi,'/gu/reports/seller/operation/orders',methods=['GET','POST'])
api.add_resource(GuReportsSellerAndOperationForwardingExcelApi,'/gu/reports/seller/operation/forwarding',methods=['GET','POST'])
api.add_resource(SeleksiyonUrunEtiketApi,'/seleksiyon/etiket/excel',methods=['GET','POST'])


if __name__ == '__main__':
    app.run(port=5000,debug=True)