from api.sql import *
from api.date import *
from model.cost import *
from api.currency import *

class Odemeler:

    def __init__(self):

        self.data = SqlConnect().data

        self.dtOdemeler = self.data.getList( # bu liste ödemeleri gösterir

            """
                  Select
            o.Tarih,
            o.SiparisNo, 
            o.Masraf,
			sum(o.Tutar) as tutar,
            o.Kur
            from
            OdemelerTB o,MusterilerTB m
            where m.ID=o.MusteriID and m.Marketing='Mekmar'
            and o.SiparisNo in (
                Select s.SiparisNo from SiparislerTB s
                where s.SiparisNo=o.SiparisNo
                and s.MusteriID=m.ID
                and s.SiparisDurumID=3  
				
                     
            )            
			group by o.Tarih , o.SiparisNo,  o.Masraf , o.Kur
            order by o.Tarih asc
         
           
            """
        )

        self.odeme_listesi = list()

        self.__odemeListesiOlustur()
        
    def __odemeListesiOlustur(self):

        tarihIslem = TarihIslemler()
        for item in self.dtOdemeler:

            model = OzelMaliyetListeModel()
            
            if item.Tarih != None:
                model.odeme_tarihi = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            model.siparis_no = item.SiparisNo 

            if item.Masraf != None:
                model.banka_masrafi = item.Masraf
            if item.Kur != None :
                model.doviz_kur = item.Kur    
            if item.tutar != None:
                 model.odenen_toplam_tutar = item.tutar
                 

                 self.odeme_listesi.append(model)

    def getOdemeBankaMasrafi(self,siparisno):

        masraf = 0
        
        for item in self.odeme_listesi:            

            if siparisno == item.siparis_no:
                masraf += item.banka_masrafi

        return masraf

    def getOdemeBankaTRY(self,siparisno):

        odeme = 0
        usd_odeme = 0
        
        for item in self.odeme_listesi:            
           
            if siparisno == item.siparis_no:
              
                odeme += item.doviz_kur * item.odenen_toplam_tutar
                usd_odeme += item.odenen_toplam_tutar

        return odeme,usd_odeme

    def getOdemeTarih(self,siparisno):

        tarih = ''

        for item in self.odeme_listesi:

            if siparisno == item.siparis_no:
                tarih = item.odeme_tarihi # bu tarihte en son gelen paranın tarihi gösterir

        return tarih
                 
    def getOdenenToplamMasrafi(self,siparisno):

        toplam_odeme = 0
        
        for item in self.odeme_listesi:            

            if siparisno == item.siparis_no:
                toplam_odeme += item.odenen_toplam_tutar

        return toplam_odeme      

    def getOdenenKur(self,siparisno,odenen,year,month,day):
        doviz_kur = 0
       
        if odenen > 0:
             
            for item in self.odeme_listesi:            
            
                if siparisno == item.siparis_no:
                    doviz_kur = item.doviz_kur
            
                        

        
            return (doviz_kur)
        else:
            doviz = DovizListem()
            dovizKur = doviz.getDovizKurListe(str(year),str(month),str(day))
            return dovizKur

class OdemelerKar:
    def __init__(self,yil):
        self.yil = yil
        self.odemeler_listesi = list()
        self.data = SqlConnect().data
        self.__odemeler_listes_olustur()
    def __odemeler_listes_olustur(self):
        odemeler_list = self.data.getList("""
                                                select 
                                                    o.SiparisNo,
													sum(o.Tutar) as GelenBedelUsd,
                                                    sum(o.Masraf) as BankaMasrafi,
                                                    sum(o.Tutar * o.Kur) as GelenBedelTR,
													(sum(o.Kur) / count(o.SiparisNo)) as OrtKur
                                                from
                                                    OdemelerTB o
                                                    inner join SiparislerTB s on s.SiparisNo= o.SiparisNo
                                                    inner join MusterilerTB m on m.ID = s.MusteriID
                                                where
                                                    m.Marketing = 'Mekmar' and
                                                    s.SiparisDurumID= 3
												group by
													o.SiparisNo

                                               """)
        for item in odemeler_list:
            model = OzelMaliyetListeKarModel()
            model.siparis_no = item.SiparisNo
            model.banka_masrafi = self.__noneControl(item.BankaMasrafi)
            model.odenen_usd_tutar = self.__noneControl(item.GelenBedelUsd)
            model.odenen_try_tutar = self.__noneControl(item.GelenBedelTR)
            model.ortalama_kur = self.__noneControl(item.OrtKur)
            self.odemeler_listesi.append(model)
    
    def getOdemelerModel(self,siparis_no):
        model = OzelMaliyetListeKarModel()
        for item in self.odemeler_listesi:
            if(item.siparis_no == siparis_no):
                model.siparis_no = item.siparis_no
                model.banka_masrafi = item.banka_masrafi
                model.odenen_usd_tutar = item.odenen_usd_tutar
                model.odenen_try_tutar = item.odenen_try_tutar
                model.ortalama_kur = item.ortalama_kur
        return model
            
    def __noneControl(self,value):
        if(value == None):
            return 0 
        else:
            return float(value)