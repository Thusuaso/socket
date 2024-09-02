from api.sql import *
from model.cost import *
 

class Urunler:

    def __init__(self,yil,ay):

        self.data = SqlConnect().data

        self.dtUrunler = self.data.getStoreList(
            """
            select
            u.SiparisNo,
            u.SatisToplam,
            (u.AlisFiyati * u.Miktar) as AlisToplam,
            u.TedarikciID
            from
            SiparisUrunTB u

            where
            u.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID and u.SiparisNo=s.SiparisNo
            and s.SiparisDurumID=3 and m.Marketing='Mekmar'
            and Year(s.YuklemeTarihi)=? 
            and Month(s.YuklemeTarihi)=?
            )

            """,(yil,ay)
        )

        self.dtFaturalar = self.data.getList(

            """
            select * from Tedarikci_Siparis_FaturaTB
            """

        )
        
        self.urunler_listesi = list()

        self.__urunListesiOlustur()
    #Mekmer Id 1 Mekmoz ıd 123

    def __urunListesiOlustur(self):

        for item in self.dtUrunler:

            model = OzelMaliyetListeModel()
            model.siparis_no = item.SiparisNo
            model.dis_alim_fatura_list = self.__getDisAlimFaturaSayisi(item.TedarikciID,item.SiparisNo)
            if item.AlisToplam != None:
                if item.TedarikciID == 1 or item.TedarikciID == 123:
                    if item.TedarikciID == 1:
                        model.mekmar_alim = item.AlisToplam
                        model.mekmar_alim_evrak = self.__getMekmarFatura(item.SiparisNo)


                    if item.TedarikciID == 123:
                        model.mekmoz_alim = item.AlisToplam
                        model.mekmoz_alim_evrak = self.__getMekmozFatura(item.SiparisNo)

                else:
                    model.dis_alim = item.AlisToplam


                    
                    
                model.dis_alim_evrak = self.__getDisFirmaFaturalar(item.SiparisNo,item.TedarikciID)




            if(item.AlisToplam == None or item.AlisToplam == 0 or item.AlisToplam == ' ' or item.AlisToplam == 'null' or item.AlisToplam == '' or str(item.AlisToplam) == '0E-11' or item.AlisToplam == 0E-11): 
                if item.TedarikciID == 1 or item.TedarikciID == 123:
                    if item.TedarikciID == 1:
                        model.mekmer_alim_alis_kontrol += 1

                    if item.TedarikciID == 123:
                        model.mekmoz_alim_alis_kontrol += 1

                else:
                    model.dis_alim_alis_kontrol += 1

            if item.SatisToplam != None:
                model.toplam_bedel = item.SatisToplam









            self.urunler_listesi.append(model)
          
    def getUrunModel(self,siparisNo):

        model = OzelMaliyetListeModel()

        for item in self.urunler_listesi:

            if siparisNo == item.siparis_no:
                model.toplam_bedel += item.toplam_bedel
                model.mekmar_alim += item.mekmar_alim
                model.mekmoz_alim += item.mekmoz_alim
                model.dis_alim += item.dis_alim
                model.mekmer_alim_alis_kontrol += item.mekmer_alim_alis_kontrol
                model.mekmoz_alim_alis_kontrol += item.mekmoz_alim_alis_kontrol
                model.dis_alim_alis_kontrol += item.dis_alim_alis_kontrol



                #model.mekmar_alim_evrak = item.mekmar_alim_evrak
                #model.mekmoz_alim_evrak = item.mekmoz_alim_evrak
                #model.dis_alim_evrak = item.dis_alim_evrak
                model.dis_alim_fatura_sayisi = item.dis_alim_fatura_sayisi
                

                

        return model      

    def __getDisAlimFaturaSayisi(self,tedarikci_id,siparis_no):
    
        liste = list()

        for item in self.dtUrunler:
            
            if siparis_no == item.SiparisNo:
                if item.TedarikciID != 1 or item.TedarikciID != 123:
                    liste.append(item)

        return liste

    def __getDisFirmaFaturalar(self,siparis_no,tedarikci_id):

        liste = list()
        id = 1
        for item in self.dtFaturalar:

            if item.SiparisNo == siparis_no and item.TedarikciID == tedarikci_id:
                 model = TedarikciFaturaModel()
                 model.id = id
                 model.link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"
                 model.evrak_adi = item.FaturaNo
                 liste.append(model)
        
        return liste
    
    def __getMekmarFatura(self,siparis_no):

        link = ''

        for item in self.dtFaturalar:

            if item.TedarikciID == 1 and item.SiparisNo == siparis_no:
                link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"

        return link

    def __getMekmozFatura(self,siparis_no):

        link = ''

        for item in self.dtFaturalar:

            if item.TedarikciID == 123 and item.SiparisNo == siparis_no:
                link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"

        return link


class Urunler_Yil:

    def __init__(self,yil):

        self.data = SqlConnect().data

        self.dtUrunler = self.data.getStoreList(
            """
            select
            u.SiparisNo,
            u.SatisToplam,
            (u.AlisFiyati * u.Miktar) as AlisToplam,
            u.TedarikciID
            from
            SiparisUrunTB u

            where
            u.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID and u.SiparisNo=s.SiparisNo
            and s.SiparisDurumID=3 and m.Marketing='Mekmar'
            and Year(s.YuklemeTarihi)=?             
            )

            """,(yil)
        )

        self.dtFaturalar = self.data.getList(

            """
            select * from Tedarikci_Siparis_FaturaTB
            """

        )

        self.urunler_listesi = list()

        self.__urunListesiOlustur()
    #Mekmer Id 1 Mekmoz ıd 123

    def __urunListesiOlustur(self):

        for item in self.dtUrunler:

            model = OzelMaliyetListeModel()
            model.siparis_no = item.SiparisNo
            model.dis_alim_fatura_sayisi = self.__getDisAlimFaturaSayisi(item.TedarikciID,item.SiparisNo)            
            if item.AlisToplam != None:
                if item.TedarikciID == 1 or item.TedarikciID == 123:
                    if item.TedarikciID == 1:
                        model.mekmar_alim = item.AlisToplam
                        model.mekmar_alim_evrak = self.__getMekmarFatura(item.SiparisNo)
                    if item.TedarikciID == 123:
                        model.mekmoz_alim = item.AlisToplam
                        model.mekmoz_alim_evrak = self.__getMekmozFatura(item.SiparisNo)
                else:
                    model.dis_alim = item.AlisToplam
                    model.dis_alim_evrak =  self.__getDisFirmaFaturalar(item.SiparisNo,item.TedarikciID)
            

            if (item.AlisToplam == None or item.AlisToplam == 0 or item.AlisToplam == ' ' or item.AlisToplam == 'null' or item.AlisToplam == '' or str(item.AlisToplam) == '0E-11' or item.AlisToplam == 0E-11): 
                if item.TedarikciID == 1 or item.TedarikciID == 123:
                    if item.TedarikciID == 1:
                        model.mekmer_alim_alis_kontrol += 1

                    if item.TedarikciID == 123:
                        model.mekmoz_alim_alis_kontrol += 1

                else:
                    model.dis_alim_alis_kontrol += 1




            if item.SatisToplam != None:
                model.toplam_bedel = item.SatisToplam

            self.urunler_listesi.append(model)
           
    
    def getUrunModel(self,siparisNo):

        model = OzelMaliyetListeModel()

        for item in self.urunler_listesi:
            if siparisNo == item.siparis_no:
                model.toplam_bedel += item.toplam_bedel
                model.mekmar_alim += item.mekmar_alim
                model.mekmoz_alim += item.mekmoz_alim
                model.dis_alim += item.dis_alim
                model.mekmar_alim_evrak = item.mekmar_alim_evrak
                model.mekmoz_alim_evrak = item.mekmoz_alim_evrak
                model.dis_alim_evrak = item.dis_alim_evrak
                model.dis_alim_fatura_sayisi += item.dis_alim_fatura_sayisi
                model.mekmer_alim_alis_kontrol += item.mekmer_alim_alis_kontrol
                model.mekmoz_alim_alis_kontrol += item.mekmoz_alim_alis_kontrol
                model.dis_alim_alis_kontrol += item.dis_alim_alis_kontrol

                

        return model 

    def __getDisAlimFaturaSayisi(self,tedarikci_id,siparis_no):

        fatura_sayisi = 0

        for item in self.dtUrunler:
           
            if siparis_no == item.SiparisNo:
                if item.TedarikciID != 1 or item.TedarikciID != 123:

                    fatura_sayisi += 1

        return fatura_sayisi




    def __getDisFirmaFaturalar(self,siparis_no,tedarikci_id):

        liste = list()
        id = 1
       
        for item in self.dtFaturalar:

            if item.SiparisNo == siparis_no and item.TedarikciID == tedarikci_id:
                 model = TedarikciFaturaModel()
                 model.id = id
                 model.link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"
                 model.evrak_adi = item.FaturaNo
                 liste.append(model)
                 
        
        return liste
    
    def __getMekmarFatura(self,siparis_no):

        link = ''

        for item in self.dtFaturalar:

            if item.TedarikciID == 1 and item.SiparisNo == siparis_no:
                link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"

        return link

    def __getMekmozFatura(self,siparis_no):

        link = ''

        for item in self.dtFaturalar:

            if item.TedarikciID == 123 and item.SiparisNo == siparis_no:
                link = f"https://file-service.mekmar.com/file/tedarikci/download/30/{siparis_no}/{item.FaturaNo}.pdf"

        return link
 
 
class UrunlerKar:
    def __init__(self,yil):
        self.yil = yil
        self.urunler_list = list()
        self.data = SqlConnect().data
        self.__urunListesiOlustur()

    def __urunListesiOlustur(self):
        urunler_listesi = self.data.getStoreList("""
                                                    select 
														s.SiparisNo,
                                                        sum(su.SatisToplam) as SatisToplami,
                                                        sum(su.AlisFiyati * su.Miktar) as AlisToplami

                                                    from 

                                                        SiparisUrunTB su
                                                        inner join SiparislerTB s on s.SiparisNo= su.SiparisNo
                                                        inner join MusterilerTB m on m.ID = s.MusteriID
                                                    where 
                                                        YEAR(s.YuklemeTarihi) = ? and
                                                        s.SiparisDurumID = 3 and
                                                        m.Marketing='Mekmar'

                                                    group by
                                                        s.SiparisNo
                                                 
                                                 """,(self.yil))
        
        for item in urunler_listesi:
            model =  OzelMaliyetListeKarModel()
            model.siparis_no = item.SiparisNo
            model.satis_toplami = self.__noneControl(item.SatisToplami)
            model.alis_toplami = self.__noneControl(item.AlisToplami)
            
            self.urunler_list.append(model)
    
    def getUrunModel(self,siparis_no):
        model = OzelMaliyetListeKarModel()
        for item in self.urunler_list:
            if(item.siparis_no == siparis_no):
                model.siparis_no = item.siparis_no
                model.satis_toplami = item.satis_toplami
                model.alis_toplami = item.alis_toplami
        return model
    
    
    def __noneControl(self,value):
        if(value == None):
            return 0
        else:
            return float(value)

    
    