from model.cost import *
from api.sql import *


class EvrakListeler:

    def __init__(self):

        self.data = SqlConnect().data

        self.dtNakliyeFaturalar = self.data.getList(

                """
                select *,(select f.FirmaAdi from FirmalarTB f where f.ID=n.FirmaID ) as firma from NakliyeFaturaKayitTB n
                """

            )
        self.dtFaturalar = self.data.getList(
            """
          select * , (select f.FirmaAdi  from FirmalarTB f  where f.ID=k.FirmaID) as firma from KonteynerDigerFaturalarKayitTB k
            """
        )  
        self.dtOzelIscilikFaturalar = self.data.getList(
            """
            select *,(select t.FirmaAdi from TedarikciTB t  where t.ID=o.TedarikciID ) as tedarikci from SiparisEkstraGiderlerTB o
            """
        )   
        self.dtMasraflar = self.data.getList(
            """
            select
            *
            from
            SiparisFaturaKayitTB f
            where f.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s,MusterilerTB m
                where m.ID=s.MusteriID and s.SiparisNo=f.SiparisNo
               
               
            )
            
            """
        )  
    def __getNakliyeFirmaId(self,fatura_id):

        firma_id = None
        firma_adi = ""

        for item in self.dtNakliyeFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID
                firma_adi = item.firma

        return firma_id   ,firma_adi

    def __getNavlun(self,siparis_no):

        evrak = ''
        adi = ""
        
        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo:               
              
                firma_id , adi= self.__getFirmaId(item.FaturaKayitID)
                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,adi

    def __getGumruk(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:
           
            if item.YuklemeEvrakID == 70 and siparis_no == item.SiparisNo and item.Tutar != None: 
                            
                tutar += item.Tutar
                firma_id , firma= self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                   
                    
        return evrak  ,firma  

    def __getNakliye(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 13 and siparis_no == item.SiparisNo and item.Tutar != None:               
                tutar += item.Tutar
                firma_id  ,firma_adi= self.__getNakliyeFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                    firma_adi = firma_adi
                    
        return evrak ,firma_adi
    
    def __getFirmaId(self,fatura_id):

        firma_id = None
        firma = ""

        for item in self.dtFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID
                firma = item.firma

        return firma_id , firma

    def __getNakliyeFirmaId(self,fatura_id):

        firma_id = None
        firma_adi = ""

        for item in self.dtNakliyeFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID
                firma_adi = item.firma

        return firma_id,firma_adi

    def __getOzelIscilikFirmaId(self,siparisNo):

        firma_adi = None

        for item in self.dtOzelIscilikFaturalar:

            if siparisNo == item.SiparisNo:
                firma_adi = item.tedarikci

        return firma_adi     
        
    def __getLiman(self,siparis_no):
       
        evrak = ''
        tutar = 0
        firma = ""
        for item in self.dtMasraflar:
           
            if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
            
                firma_id  , firma = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                   
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                    
        return evrak , firma

    def __getIlaclama(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:
           
            if item.SiparisFaturaTurID == 73 and siparis_no == item.SiparisNo and item.Tutar != None:             
                tutar += item.Tutar
                firma_id ,firma = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak , firma

    def getSiparisListe(self):

        result = self.data.getList(
            """
               select
                    * ,
                (select m.FirmaAdi from MusterilerTB m where m.ID = s.MusteriID) as MusteriAdi,
                (select m.MailAdresi from MusterilerTB m where m.ID = s.MusteriID) as mail,
                (select o.OdemeTur from OdemeTurTB o where o.ID = s.OdemeTurID) as odemeTuru,
                (select t.TeslimTur from SiparisTeslimTurTB t where t.ID=s.TeslimTurID ) as teslimTuru
              from
                SiparislerTB s
                where s.SiparisDurumID!=1
                and year(s.SiparisTarihi) in (2024,2023,2022,2021 ,2020)
                order by s.SiparisTarihi desc

            """
        )

        liste = list()

        for item in result: 

            model = EvrakSiparisListeModel()
            model.id = item.ID 
            model.siparisno = item.SiparisNo
            model.musteriid = item.MusteriID
            model.mail = item.mail
            model.musteriAdi = item.MusteriAdi
            model.odeme = item.odemeTuru
            model.teslim = item.teslimTuru
            model.ulke = item.Ulke
            model.eta = item.Eta
            model.KonteynerNo = item.KonteynerNo
            model.line = item.Line
            model.navlunAlis = item.NavlunAlis
            model.navlunSatis = item.NavlunSatis
            liste.append(model)

        schema = EvrakSiparisListeSchema(many=True)

        return schema.dump(liste)

    def getEvrakTurListe(self):

        result = self.data.getList(
            """
           select * from YeniYuklemeEvraklarTB

            """
        )

        liste = list()

        for item in result: 

            model = EvrakListeModel()
            model.Faturaid = item.ID 
            model.faturaadi = item.EvrakAdi
            model.renk = "gray"
            

            liste.append(model)

        schema = EvrakListeSchema(many=True)

        return schema.dump(liste)

    def getEvrakRenkListe(self,siparis_no):

        result = self.data.getList(
            """
           select * from YeniYuklemeEvraklarTB

            """
        )

        liste = list()

        for item in result: 

            model = EvrakListeModel()
            model.Faturaid = item.ID 
            model.faturaadi = item.EvrakAdi
          
            model.renk = self.__durumRenk(siparis_no , item.ID)

            liste.append(model)

        schema = EvrakListeSchema(many=True)

        return schema.dump(liste)      

    def __durumRenk(self,siparis_no,fatura_id):   

          result = self.data.getStoreList(
            """
            select  count(*) as durum from SiparisFaturaKayitTB where  SiparisNo=? AND YuklemeEvrakID= ?

            """,(siparis_no, fatura_id)
        )[0].durum
         
          color = "red"
          if result >=1 :
              color = "green"
         
          return color
          
         
          
    def getEvrakList(self,siparisNo):

        result = self.data.getStoreList(
            """
       select
            *,
            
			(select k.KullaniciAdi from KullaniciTB k where k.ID=f.KullaniciID) as kullanici
            from
            SiparisFaturaKayitTB f
            where f.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s,MusterilerTB m
                where m.ID=s.MusteriID and s.SiparisNo=f.SiparisNo
            
               
              
				and f.SiparisNo=?
            )
            order by YuklemeEvrakID ASC
            """,(siparisNo)
        )

        liste = list()
       
        id = 0 
        for item in result:
            
            model = FaturaListeModel()
            model.faturano = item.YuklemeEvrakID
            model.faturaId = item.ID
            model.id = id
            model.yuklemeTarihi = item.EvrakYuklemeTarihi
            model.kullanici = item.kullanici
            model.siparisNo = siparisNo
            if item.YuklemeEvrakID == 1 :
              model.Draft =  f"https://file-service.mekmar.com/file/download/1/{item.SiparisNo}"
              model.adi = 'Purchase Order'
            
            if item.YuklemeEvrakID == 2 :
             model.Draft =  f"https://file-service.mekmar.com/file/download/2/{item.SiparisNo}"
             model.adi = 'Proforma Invoice'
             
            if item.YuklemeEvrakID == 3 and item.Evrak_Kontrol != 1:
             if ( item.YeniEvrakID ) : 
                 model.faturano = item.YeniEvrakID
             model.Draft =  f"https://file-service.mekmar.com/file/download/3/{item.SiparisNo}"
             model.adi = item.EvrakAdi
             model.adi = "ISF -" + model.adi
             model.evrakadi = item.EvrakAdi.split('-')[0]
             model.yeniID = item.YuklemeEvrakID
          

            if item.YuklemeEvrakID == 3  and item.Evrak_Kontrol == 1:
              if ( item.YeniEvrakID ) : 
                   model.faturano = item.YeniEvrakID
              model.Draft =  f"https://file-service.mekmar.com/file/download/3/{item.EvrakAdi}"
              model.adi = item.EvrakAdi
              model.adi = "ISF -" + model.adi
              model.evrakadi = item.EvrakAdi.split('-')[0]
              model.yeniID = item.YuklemeEvrakID

            if item.YuklemeEvrakID == 4 :
             model.Draft =  f"https://file-service.mekmar.com/file/download/4/{item.SiparisNo}"
             model.adi = 'Çeki Listesi'

            if item.YuklemeEvrakID == 5 :
             model.Draft =  f"https://file-service.mekmar.com/file/download/5/{item.SiparisNo}"
             model.adi = 'Yükleme Notası'

            if item.YuklemeEvrakID == 6 :
                model.Draft =  f"https://file-service.mekmar.com/file/download/6/{item.SiparisNo}"
                model.adi = 'Mekmar/Efes Gümrük Faturası'
            
            if item.YuklemeEvrakID == 7 :
             model.Draft =  f"https://file-service.mekmar.com/file/download/7/{item.SiparisNo}"
             model.adi = 'Gümrük Notası'

            if item.YuklemeEvrakID == 8 :
             model.Draft=  f"https://file-service.mekmar.com/file/download/8/{item.SiparisNo}"
             model.adi = 'ISF vb Formlar'

            if item.YuklemeEvrakID == 9 :
             model.Draft=  f"https://file-service.mekmar.com/file/download/9/{item.SiparisNo}"
             model.adi = 'Konşimento'

            if item.YuklemeEvrakID == 10 :
             model.Draft=  f"https://file-service.mekmar.com/file/download/10/{item.SiparisNo}"
             model.adi = 'İlaçlama Belgesi'

            if item.YuklemeEvrakID == 11 :
             model.Draft=  f"https://file-service.mekmar.com/file/download/11/{item.SiparisNo}"
             model.adi = 'Dolaşım Belgeleri'

            if item.YuklemeEvrakID == 12 :
             model.Draft=  f"https://file-service.mekmar.com/file/download/12/{item.SiparisNo}"
             model.adi = 'Gçb Beyannamesi (Export Declaration)'



            if item.YuklemeEvrakID == 14:
             model.Draft=  f"https://file-service.mekmar.com/file/download/14/{item.SiparisNo}"  
             model.adi = 'Packing Declarition'

            if item.YuklemeEvrakID == 15:
             model.Draft=  f"https://file-service.mekmar.com/file/download/15/{item.SiparisNo}"
             model.adi = 'L-C Metin'

            if item.YuklemeEvrakID == 16:
              model.Draft =  f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"
              model.adi = 'Commer Invoice'  

            if item.YuklemeEvrakID == 17:
              model.Draft =  f"https://file-service.mekmar.com/file/download/17/{item.SiparisNo}" 
              model.adi = 'Packing List'

            if item.YuklemeEvrakID == 20:
              model.Draft =  f"https://file-service.mekmar.com/file/download/20/{item.SiparisNo}" 
              model.adi = 'Booking'

            if item.YuklemeEvrakID == 30:
                if ( item.YeniEvrakID ) : 
                   model.faturano = item.YeniEvrakID
                model.adi = item.EvrakAdi
                model.adi = "Tedarikçi - " +model.adi
                model.Draft =  f"https://file-service.mekmar.com/file/tedarikci/download/30/{item.SiparisNo}/{item.EvrakAdi}"
              
            if item.YuklemeEvrakID == 13:
                firma_id , firma = self.__getNakliyeFirmaId(item.FaturaKayitID)
                if firma_id != None:
                    if ( item.YeniEvrakID ) : 
                        model.faturano = item.YeniEvrakID
                        model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                        model.adi = firma
                        model.adi = "Nakliye -"+ model.adi

            if item.YuklemeEvrakID == 40:
                if ( item.YeniEvrakID ) : 
                   model.faturano = item.YeniEvrakID

                model.adi = "Özel İşçilik"
              
                model.Draft =  f"https://file-service.mekmar.com/file/download/40/{item.SiparisNo}"
               
           

            if item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50:
                    
                    firma_id , firma = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        if ( item.YeniEvrakID ) : 
                            model.faturano = item.YeniEvrakID
                        model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                        model.adi = firma
                        model.adi = "Denizcilik Faturası -"+ model.adi


            if item.YuklemeEvrakID == 50 and  item.SiparisFaturaTurID == 13:
                    
                    firma_id , firma = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        if ( item.YeniEvrakID ) : 
                            model.faturano = item.YeniEvrakID
                        model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                        model.adi = firma
                        model.adi = "Navlun -" + model.adi

            if item.YuklemeEvrakID == 70 and item.SiparisFaturaTurID == 7:
                 for item1 in self.dtMasraflar:
           
                        if item.YuklemeEvrakID == 70 and item.SiparisNo == item1.SiparisNo and item.Tutar != None: 
                            
                           
                             firma_id,firma  = self.__getFirmaId(item.FaturaKayitID)

                             if firma_id != None:
                                if ( item.YeniEvrakID ) : 
                                    model.faturano = item.YeniEvrakID
                                model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                                model.adi = firma

              
             
              
            

            if item.YuklemeEvrakID == 71:
               model.Draft =  f"https://file-service.mekmar.com/file/download/71/{item.SiparisNo}"  
               model.adi = 'İlaçlama Notası' 
            
            if item.YuklemeEvrakID == 72:
               model.Draft =  f"https://file-service.mekmar.com/file/download/72/{item.SiparisNo}" 
               model.adi = 'Fotolar'
               
            if item.SiparisFaturaTurID == 73:
               model.Draft,firma =  self.__getIlaclama(siparisNo)
               model.adi = firma  
               

            if item.YuklemeEvrakID == 99:
               model.Draft =  f"https://file-service.mekmar.com/file/download/99/{item.SiparisNo}"
               model.adi = 'Draft'
               
            if item.SiparisFaturaTurID == 101:
                firma_id,firma  = self.__getFirmaId(item.FaturaKayitID)
                model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                model.adi = firma + ' ' + 'Booking'
                
            if item.SiparisFaturaTurID == 102:
                firma_id,firma  = self.__getFirmaId(item.FaturaKayitID)
                model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                model.adi = firma + ' ' + 'Spanzet'
                                        
            if item.SiparisFaturaTurID == 100:
                firma_id,firma  = self.__getFirmaId(item.FaturaKayitID)
                model.Draft = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                model.adi = firma + ' ' + 'Lashing'
                

            id = id +1
            model.evrak_id = item.YuklemeEvrakID
            liste.append(model)
        
        schema = FaturaListeSchema(many=True)
        
        return schema.dump(liste)
    

    def getTedarikciList(self,siparisNo):

        result = self.data.getStoreList(
            """
             select 
             s.SiparisNo,t.FirmaAdi , t.ID
             from SiparisUrunTB s , TedarikciTB t 
             where 
             t.ID = s.TedarikciID  
             and s.SiparisNo=?
              group by t.FirmaAdi,s.SiparisNo , t.ID
            """,(siparisNo)
        )
        liste = list()

        for item in result: 

            model = TedarikciModel()
            model.ID = item.ID
            model.siparisno = item.SiparisNo
            model.tedarikci = item.FirmaAdi

            liste.append(model)

        schema = TedarikciSchema(many=True)

        return schema.dump(liste)
    
    def getIscilikTedarikciList(self,po):
        try:
            result = self.data.getStoreList("""
                                                select 
                                                    se.SiparisNo,
                                                    (select t.ID from TedarikciTB t where t.ID = se.TedarikciID) as ID,
                                                    (select t.FirmaAdi from TedarikciTB t where t.ID = se.TedarikciID) as FirmaAdi


                                                from SiparisEkstraGiderlerTB se

                                                where se.SiparisNo=?
                                            """,(po))

            liste = list()
            for item in result: 

                model = TedarikciModel()
                model.ID = item.ID
                model.siparisno = item.SiparisNo
                model.tedarikci = item.FirmaAdi

                liste.append(model)

            schema = TedarikciSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getIscilikTedarikciList hata',str(e))
            return False

                
                
            