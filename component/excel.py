from openpyxl import *
import shutil


class ExcelCiktiIslem:

    def maliyet_rapor_ciktisi(self,data_list):

            try:
                source_path = 'resource_api/maliyet_raporlar/sablonlar/ayo_maliyet_listesi.xlsx'
                target_path = 'resource_api/maliyet_raporlar/dosyalar/ayo_maliyet_listesi.xlsx'

                shutil.copy2(source_path, target_path)

               
                kitap = load_workbook(target_path)
                sayfa = kitap.get_sheet_by_name('Sheet')

                satir = 2

                for item in data_list:
                    sayfa.cell(satir,column=1,value=item['siparisci'])
                    sayfa.cell(satir,column=2,value=item['operasyon'])
                    sayfa.cell(satir,column=3,value=item['siparis_no'])
                    sayfa.cell(satir,column=4,value=item['marketing'])
                    sayfa.cell(satir,column=5,value=item['faturatur'])
                    sayfa.cell(satir,column=6,value=item['siparis_tarihi'])             
                    sayfa.cell(satir,column=7,value=item['yukleme_tarihi'])
                    sayfa.cell(satir,column=8,value=item['musteri_adi'])
                    sayfa.cell(satir,column=9,value=item['ulke_adi'])
                    sayfa.cell(satir,column=10,value=item['teslim_sekli'])
                    sayfa.cell(satir,column=11,value=item['toplam_bedel'])
                    sayfa.cell(satir,column=12,value=item['mekmar_alim'])
                    sayfa.cell(satir,column=13,value=item['mekmoz_alim'])
                    sayfa.cell(satir,column=14,value=item['dis_alim'])
                    sayfa.cell(satir,column=15,value=item['nakliye'])
                    sayfa.cell(satir,column=16,value=item['gumruk'])
                    sayfa.cell(satir,column=17,value=item['ilaclama'])
                    sayfa.cell(satir,column=18,value=item['liman'])
                    sayfa.cell(satir,column=19,value=item['sigorta'])
                    sayfa.cell(satir,column=20,value=item['navlun'])
                    sayfa.cell(satir,column=21,value=item['detay_1'])
                    sayfa.cell(satir,column=22,value=item['detay_2'])
                    sayfa.cell(satir,column=23,value=item['detay_3'])
                    sayfa.cell(satir,column=24,value=item['mekus_masraf'])
                   
                   
                    sayfa.cell(satir,column=25,value=item['pazarlama'])
                    sayfa.cell(satir,column=26,value=item['ozel_iscilik'])
                    sayfa.cell(satir,column=27,value=item['banka_masrafi'])
                    sayfa.cell(satir,column=28,value=item['kurye_masrafi'])
                    sayfa.cell(satir,column=29,value=item['masraf_toplam'])
                    sayfa.cell(satir,column=30,value=item['kar_zarar'])
                    sayfa.cell(satir,column=31,value=item['kar_zarar_tl'])
                
                    sayfa.cell(satir,column=32,value=item['dosya_kapanma_date'])
                  
                    
                    
                    

                    satir += 1

                kitap.save(target_path)
                kitap.close()

                return True

            except Exception as e:
                print('ExcelCiktiIslem depoCikti Hata : ',str(e))
                return False