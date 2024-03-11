from api.sql import *
from model.cost import *


class Masraflar:

    def __init__(self,yil,ay): 

        self.data = SqlConnect().data

        self.dtMasraflar = self.data.getStoreList(
            """
            select
            *
            from
            SiparisFaturaKayitTB f
            where f.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s,MusterilerTB m
                where m.ID=s.MusteriID and s.SiparisNo=f.SiparisNo
                and s.SiparisDurumID=3
                and year(s.YuklemeTarihi)=?
                and month(s.YuklemeTarihi)=?
            )
            and f.YuklemeEvrakID in (
                70,13,73,50,16
            )
            """,(yil,ay)
        )

        self.dtFaturalar = self.data.getList(
            """
            select * from KonteynerDigerFaturalarKayitTB
            """
        )

        self.dtNakliyeFaturalar = self.data.getList(

            """
            select * from NakliyeFaturaKayitTB
            """

        )
        self.dtDovizKur = self.data.getList(
            """
           select k.Kur , s.SiparisNo from SiparisFaturaKayitTB s ,KonteynerDigerFaturalarKayitTB k where k.ID = s.FaturaKayitID
            """
        )

        self.masraf_listesi = list()

        # self.__masrafListesiOlustur()
        doviz = 0
    def __masrafListesiOlustur(self):

        for item in self.dtMasraflar:

            model = OzelMaliyetListeModel()
            model.siparis_no = item.SiparisNo
            model.evrak_id = item.YuklemeEvrakID
            model.tur_id = item.SiparisFaturaTurID
          
            if int(item.YuklemeEvrakID) == 16:
                
                model.satis_faturasi = f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"
               
                   
            if item.Tutar !=None:
                #gümrük
                if item.YuklemeEvrakID == 70:
                    model.gumruk += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.gumruk_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                #nakliye
                if item.YuklemeEvrakID == 13:
                    model.nakliye += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.nakliye_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                 #ilaçlama
                if item.SiparisFaturaTurID == 73:
                    model.ilaclama += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.ilaclama_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
               
                #sigorta
                if item.SiparisFaturaTurID == 15:
                    model.sigorta += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.sigorta_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                #liman
                if item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50:
                    model.liman += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.liman_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
               #navlun
                if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50:
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.navlun_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                   

            self.masraf_listesi.append(model)


    def getMasrafModel(self,siparis_no):

        model = OzelMaliyetListeModel()
        model.satis_faturasi = self.__getFaturaBilgi(siparis_no)
        model.gumruk_evrak,model.gumruk = self.__getGumruk(siparis_no)
        model.nakliye_evrak,model.nakliye = self.__getNakliye(siparis_no)
        model.ilaclama_evrak,model.ilaclama = self.__getIlaclama(siparis_no)
        model.liman_evrak,model.liman= self.__getLiman(siparis_no)
        model.navlun_evrak = self.__getNavlun(siparis_no)
        model.lashing_evrak,model.lashing = self.__getLashing(siparis_no)
        model.booking_evrak,model.booking = self.__getBooking(siparis_no)
        model.spazlet_evrak,model.spazlet = self.__getSpazlet(siparis_no)
        
        
        
        #model.doviz_kur = self.__getDovizBilgi(siparis_no)
       

        return model


    
    def __getFaturaBilgi(self,siparis_no):

        fatura_no = ''

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 16 and siparis_no == item.SiparisNo:
                fatura_no = f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"

        return fatura_no

    def __getDovizBilgi(self,siparis_no):

        kur = 0

        for item in self.dtDovizKur:

            if  siparis_no == item.SiparisNo:
                kur = item.Kur

        return kur
     

    def __getGumruk(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 70 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getIlaclama(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 73 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar
    def __getLashing(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 100 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getBooking(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 101 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar
    
    def __getSpazlet(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 102 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar
    
    
    def __getLiman(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

        return evrak,tutar

    def __getNavlun(self,siparis_no):

        evrak = ''

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo:               
              
                firma_id = self.__getFirmaId(item.FaturaKayitID)
                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak

    def __getNakliye(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 13 and siparis_no == item.SiparisNo and item.Tutar != None:               
                tutar += item.Tutar
                firma_id = self.__getNakliyeFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    


     

    def __getFirmaId(self,fatura_id):

        firma_id = None

        for item in self.dtFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID

        return firma_id

    def __getNakliyeFirmaId(self,fatura_id):

        firma_id = None

        for item in self.dtNakliyeFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID

        return firma_id

class Masraflar_Yil:

    def __init__(self,yil): 

        self.data = SqlConnect().data

        self.dtMasraflar = self.data.getStoreList(
            """
            select
            *
            from
            SiparisFaturaKayitTB f
            where f.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s,MusterilerTB m
                where m.ID=s.MusteriID and s.SiparisNo=f.SiparisNo
                and s.SiparisDurumID=3
                and year(s.YuklemeTarihi)=?                
            )
            and f.YuklemeEvrakID in (
                70,13,73,50,16
            )
            """,(yil)
        )

        self.dtFaturalar = self.data.getList(
            """
            select * from KonteynerDigerFaturalarKayitTB
            """
        )

        

        self.dtNakliyeFaturalar = self.data.getList(

            """
            select * from NakliyeFaturaKayitTB
            """

        )

        self.masraf_listesi = list()

        #self.__masrafListesiOlustur()

    def __masrafListesiOlustur(self):

        for item in self.dtMasraflar:

            model = OzelMaliyetListeModel()
            model.siparis_no = item.SiparisNo
            model.evrak_id = item.YuklemeEvrakID
            model.tur_id = item.SiparisFaturaTurID            
            if int(item.YuklemeEvrakID) == 16:               
                model.satis_faturasi = f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"
                
                   
            if item.Tutar !=None:
                #gümrük
                if item.YuklemeEvrakID == 70:
                    model.gumruk += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.gumruk_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                #nakliye
                if item.YuklemeEvrakID == 13:
                    model.nakliye += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.nakliye_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                 #ilaçlama
                if item.SiparisFaturaTurID == 73:
                    model.ilaclama += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.ilaclama_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                #liman
                if item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50:
                    model.liman += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.liman_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                
                if item.SiparisFaturaTurID == 100 and item.YuklemeEvrakID == 50:
                    model.lashing += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.lashing_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                
                if item.SiparisFaturaTurID == 102 and item.YuklemeEvrakID == 50:
                    model.spazlet += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.spazlet_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                
                
                if item.SiparisFaturaTurID == 101 and item.YuklemeEvrakID == 50:
                    model.booking += item.Tutar
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.booking_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"
                
                
                if item.SiparisFaturaTurID == 73 and item.YuklemeEvrakID == 50:
                    firma_id = self.__getFirmaId(item.FaturaKayitID)
                    if firma_id != None:
                        model.navlun_evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

            self.masraf_listesi.append(model)


    def getMasrafModel(self,siparis_no):

        model = OzelMaliyetListeModel()
        model.satis_faturasi = self.__getFaturaBilgi(siparis_no)
        model.gumruk_evrak,model.gumruk = self.__getGumruk(siparis_no)
        model.nakliye_evrak,model.nakliye = self.__getNakliye(siparis_no)
        model.ilaclama_evrak,model.ilaclama = self.__getIlaclama(siparis_no)
        model.liman_evrak,model.liman= self.__getLiman(siparis_no)
        model.navlun_evrak = self.__getNavlun(siparis_no)
        model.lashing_evrak,model.lashing= self.__getLashing(siparis_no)
        model.booking_evrak,model.booking= self.__getBooking(siparis_no)
        model.spazlet_evrak,model.spazlet= self.__getSpazlet(siparis_no)
        
        
      

        return model


    
    def __getFaturaBilgi(self,siparis_no):

        fatura_no = ''

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 16 and siparis_no == item.SiparisNo:
                fatura_no = f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"

        return fatura_no

   

    def __getGumruk(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 70 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getIlaclama(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 73 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getLiman(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

        return evrak,tutar

    def __getNavlun(self,siparis_no):

        evrak = ''

        for item in self.dtMasraflar:
            
            if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50 and siparis_no == item.SiparisNo:               
                firma_id = self.__getFirmaId(item.FaturaKayitID)
                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak

    def __getNakliye(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.YuklemeEvrakID == 13 and siparis_no == item.SiparisNo and item.Tutar != None:               
                tutar += item.Tutar
                firma_id = self.__getNakliyeFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getLashing(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 100 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar

    def __getBooking(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 101 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar
    
    def __getSpazlet(self,siparis_no):

        evrak = ''
        tutar = 0

        for item in self.dtMasraflar:

            if item.SiparisFaturaTurID == 102 and siparis_no == item.SiparisNo and item.Tutar != None:                
                tutar += item.Tutar
                firma_id = self.__getFirmaId(item.FaturaKayitID)

                if firma_id != None:
                    evrak = f"https://file-service.mekmar.com/file/download/customer/{firma_id}/{item.EvrakAdi}"

                    
        return evrak,tutar
    

     

    def __getFirmaId(self,fatura_id):

        firma_id = None

        for item in self.dtFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID

        return firma_id

    def __getNakliyeFirmaId(self,fatura_id):

        firma_id = None

        for item in self.dtNakliyeFaturalar:

            if fatura_id == item.ID:
                firma_id = item.FirmaID

        return firma_id

   
                

