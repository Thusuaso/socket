from api.sql import SqlConnect
from model.financedetail import *


class VadeAnaliste:

    def __init__(self):

        self.data = SqlConnect().data
      
 
    def getVadeList(self):

        result = self.data.getList(

            """
           select  
            m.FirmaAdi  ,
            dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo) as tutar,
            s.SiparisNo,
            s.Vade
            
            from  
            SiparislerTB s,MusterilerTB m  
            where   
            s.MusteriID = m.ID  
            and s.SiparisDurumID=3  
            and s.Vade is not null  
            and dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo)>0  
            group by m.FirmaAdi  ,s.SiparisNo,s.Vade
            """
        )

        liste = list()

        for item in result:

            model = VadeAnaListeModel()
            model.firmaAdi = item.FirmaAdi
            model.tutar = item.tutar
            model.siparis_no = item.SiparisNo
            model.vade_tarih = item.Vade
          

            liste.append(model)

        schema = VadeAnaListeSchema(many=True)

        return schema.dump(liste)


class VadeAnalisteYeni:

    def __init__(self):

        self.data = SqlConnect().data
      
 
    def getVadeList(self):

        result = self.data.getList(

            """
           select  
            m.FirmaAdi  ,
            dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo) as tutar,
            s.SiparisNo,
            s.Vade
            
            from  
            SiparislerTB s,MusterilerTB m  
            where   
            s.MusteriID = m.ID  
            and s.SiparisDurumID=3  
            and s.Vade is not null  
            and dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo)>0  
            group by m.FirmaAdi  ,s.SiparisNo,s.Vade
            """
        )

        liste = list()

        for item in result:

            model = VadeAnaListeModel()
            model.firmaAdi = item.FirmaAdi
            model.tutar = item.tutar
            model.siparis_no = item.SiparisNo
            model.vade_tarih = item.Vade
          

            liste.append(model)

        schema = VadeAnaListeSchema(many=True)

        return schema.dump(liste)

  
