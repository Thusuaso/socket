from flask_restful import Resource
from flask import jsonify,request,send_file
from component.finance.list import *
from component.finance.maturity import *
import datetime

class TarihIslemler:

    def getDate(self,date):
        try:
            year,month,_date = str(date).split('-')

            return datetime.datetime(int(year),int(month),int(_date))
        except:
            return None

class MusteriAyrinti:

    def __init__(self,musteriid):

        self.data = SqlConnect().data
        self.musteri_id = musteriid

    def getKonteynerAyrintiList(self): #2 ayrı tabloyu birleştirme

        yukleme_list = self.__uretilenler()
        
        for item in self.__yuklenenler():

            yukleme_list.append(item)

        schema = MusteriAyrintiSchema(many=True)

        return schema.dump(yukleme_list)
    
    def __yuklenenler(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
                        select
            s.ID,
            s.SiparisNo,
            s.YuklemeTarihi,
            s.Vade,
            s.TahminiEtaTarihi,
            m.FirmaAdi,
            s.MusteriID,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            s.Pesinat,
            (
            select Sum(Tutar) from Odemeler_MekmerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as Odeme,
            (
              select Sum(u.AlisFiyati * u.Miktar) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo and u.TedarikciID in (1,123)
            ) as UrunBedeli,
            			(
				select SUM (seg.Tutar) from SiparisEkstraGiderlerTB seg where seg.SiparisNo=s.SiparisNo and seg.TedarikciID in (1,123) and YEAR(seg.Tarih) >= YEAR(GETDATE())
			) as Iscilik    
            from
            SiparislerTB s,MusterilerTB m
            where
            s.MusteriID=m.ID
            and m.ID=?
            and s.SiparisDurumID=3
            order by s.YuklemeTarihi desc
            """,(self.musteri_id)
        )

        liste = list()

        for item in result:
            
            model = MusteriAyrintiModel()
            model.id = item.ID 
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.siparisno = item.SiparisNo 
            model.tip = "Yükleme"           
            if item.YuklemeTarihi != None:
                model.yuklemetarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%Y-%m-%d")               
            if item.Vade != None:
                model.vade = tarihIslem.getDate(item.Vade).strftime("%d-%m-%Y")
            
            if item.TahminiEtaTarihi != None:
                model.tahmini_eta = tarihIslem.getDate(item.TahminiEtaTarihi).strftime("%Y-%m-%d")  
            model.pesinat = item.Pesinat
            navlun = 0 
            tutar_1 = 0
            tutar_2 = 0
            tutar_3 = 0
            
            urun_bedel = 0
            odeme = 0
            sigorta  = 0
            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
            if item.DetayTutar_1 != None:
                tutar_1 = item.DetayTutar_1
            if item.DetayTutar_2 != None:
                tutar_2 = item.DetayTutar_2
            if item.DetayTutar_3 != None:
                tutar_3 = item.DetayTutar_3
              
            if item.UrunBedeli != None:
                urun_bedel = item.UrunBedeli
            if item.Odeme != None:
                odeme = item.Odeme
            if item.sigorta_tutar_satis != None:
                sigorta = item.sigorta_tutar_satis
            model.toplam = urun_bedel + self.__noneControl(item.Iscilik)
            model.siparis_total = model.toplam
            
            model.kalan = self.__floatControlDecimal(model.toplam - odeme)
            model.kalan2 = model.toplam - odeme
            model.odenen_tutar = odeme
            model.iscilik = self.__noneControl(item.Iscilik)
            liste.append(model)

        return liste  

    def __uretilenler(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select
            s.ID,
            s.SiparisNo,
            s.YuklemeTarihi,
            s.Vade,
            s.TahminiEtaTarihi,
            m.FirmaAdi,
            s.MusteriID,
            s.Pesinat,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            
            (
            select Sum(Tutar) from Odemeler_MekmerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as Odeme,
            (
            select Sum(u.AlisFiyati * u.Miktar) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo and u.TedarikciID in (1,123)
            ) as UrunBedeli,
                   			(
				select SUM (seg.Tutar) from SiparisEkstraGiderlerTB seg where seg.SiparisNo=s.SiparisNo and seg.TedarikciID in (1,123) and YEAR(seg.Tarih) >= YEAR(GETDATE())
			) as Iscilik 
            from
            SiparislerTB s,MusterilerTB m
            where
            s.MusteriID=m.ID
            and m.ID=?
           
            and s.SiparisDurumID in (1,2)
            """,(self.musteri_id)
        )

        liste = list()

        for item in result:
            
            model = MusteriAyrintiModel()
            model.id = item.ID 
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.siparisno = item.SiparisNo 
            model.tip = "Üretim"
            if item.YuklemeTarihi != None:
                model.yuklemetarihi =tarihIslem.getDate(item.YuklemeTarihi).strftime("%Y-%m-%d")    
            if item.Vade != None:
                model.vade = tarihIslem.getDate(item.Vade).strftime("%d-%m-%Y")
            if item.TahminiEtaTarihi != None:
                model.tahmini_eta = tarihIslem.getDate(item.TahminiEtaTarihi).strftime("%d-%m-%Y")
           
            pesinat = 0
            navlun = 0 
            tutar_1 = 0
            tutar_2 = 0
            tutar_3 = 0
            sigorta = 0 
            urun_bedel = 0
            odeme = 0
            
            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
            if item.DetayTutar_1 != None:
                tutar_1 = item.DetayTutar_1
            if item.DetayTutar_2 != None:
                tutar_2 = item.DetayTutar_2
            if item.DetayTutar_3 != None:
                tutar_3 = item.DetayTutar_3
            
            if item.UrunBedeli != None:
                urun_bedel = item.UrunBedeli
            if item.Pesinat != None:
                pesinat = item.Pesinat
            if item.sigorta_tutar_satis != None:
                sigorta = item.sigorta_tutar_satis
            if item.Odeme != None:
                odeme = item.Odeme
            model.pesinat = pesinat
            model.siparis_total =urun_bedel
            model.toplam = urun_bedel + self.__noneControl(item.Iscilik)
            model.kalan2 = model.siparis_total
            model.kalan =  (model.siparis_total + self.__noneControl(item.Iscilik)) - odeme
            model.odenen_tutar = odeme
            model.iscilik = self.__noneControl(item.Iscilik)
            liste.append(model)

        return liste      









    def __floatControlDecimal(self,value):
        if(value >= -8 and value <= 8):
            return 0
        else:
            return value
    def getOdemeListesi(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
 select
            o.Tarih,
            sum(o.Tutar) as Tutar
            from
            Odemeler_MekmerTB o
            where o.MusteriID=?
            and o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s
            where s.SiparisNo=o.SiparisNo
            and s.MusteriID=?
            )
            group by o.Tarih
            order by o.Tarih desc
                        """,(self.musteri_id,self.musteri_id)
        )

        liste = list()

        key = 1

        for item in result:

            model = MusteriOdemeModel()
            model.id = key
            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%Y-%m-%d")

            model.tutar = item.Tutar          
            liste.append(model)

            key += 1

        schema = MusteriOdemeSchema(many=True)

        return schema.dump(liste)

    def getOdemeSecimPoList(self,tarih):
        
        tarih = tarih
        forMat = '%d-%m-%Y'
        tarih = datetime.datetime.strptime(tarih, forMat)
        tarih = tarih.date()
        result = self.data.getStoreList(
            """
            select
            o.ID,
            o.SiparisNo,
            o.Tutar,
            o.Aciklama,
            o.Masraf,
            o.Kur,
		    (select t.OdemeTur from OdemeTurTB t where t.ID=o.FinansOdemeTurID) as tur
            from
            Odemeler_MekmerTB o
            where o.MusteriID=?
            and o.Tarih=?
            and o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s
            where s.SiparisNo=o.SiparisNo
            and s.MusteriID=o.MusteriID
            )
            """,(self.musteri_id,tarih)
        )

        liste = list()
        key = 0
        for item in result:

            model = MusteriOdemeSecimModel()
            model.id = item.ID
            model.siparisno = item.SiparisNo
            model.tutar = item.Tutar
            model.aciklama = item.Aciklama
            model.masraf = item.Masraf
            model.faturatur = item.tur
            model.kur = item.Kur
            key +=1
            model.sira = key 
            
          
            liste.append(model)

        schema = MusteriOdemeSecimSchema(many=True)

        return schema.dump(liste)

    def getByCustomersPo(self):
        try:
            result = self.data.getStoreList("""
                                   
                                    select ID,SiparisNo from SiparislerTB where MusteriID = ?
                                   """,(self.musteri_id))
            liste = list()
            for item in result:
                model = ByCustomersPoModel()
                model.id = item.ID
                model.siparisNo = item.SiparisNo
                liste.append(model)
            schema = ByCustomersPoSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print("getByCustomersPo hata",str(e))
            return False
        
    def __noneControl(self,value):
        if(value == None or value == "" or value == 'undefined' or value == 'null'):
            return 0
        else:
            return value
        
class MusteriAyrintiMonth:
    def __init__(self):
        self.data = SqlConnect().data
        
    def __noneControl(self,value):
        if(value == None or value == "" or value == 'undefined' or value == 'null'):
            return 0
        else:
            return value
    def __floatControlDecimal(self,value):
        if(value >= -8 and value <= 8):
            return 0
        else:
            return value
        
    def getKonteynerAyrintiListMonth(self,month):
        
        schema = MusteriAyrintiSchema(many=True)

        return schema.dump(self.__yuklenenlerMonth(month))

    def __yuklenenlerMonth(self,month):
        
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
                               select 

    (select sum(su.AlisFiyati * su.Miktar) from SiparisUrunTB su where su.SiparisNo = s.SiparisNo and su.TedarikciID in (1,123)) as UrunBedeli,
    m.FirmaAdi,
    s.SiparisNo,
    (select sum(om.Tutar) from Odemeler_MekmerTB om where om.SiparisNo = s.SiparisNo) as Odeme,
    (
    select SUM (seg.Tutar) from SiparisEkstraGiderlerTB seg where seg.SiparisNo=s.SiparisNo and seg.TedarikciID in (1,123)) as Iscilik,
	s.SiparisTarihi,
	s.YuklemeTarihi,
	m.ID as MusteriID


from SiparislerTB s
inner join MusterilerTB m on m.ID = s.MusteriID
inner join SiparisUrunTB sipu on sipu.SiparisNo = s.SiparisNo

where m.Marketing='Mekmar' and YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) =? and sipu.TedarikciID in (1,123)
group by s.SiparisNo,m.FirmaAdi,s.SiparisTarihi,s.YuklemeTarihi,m.ID
            """,(month)
        )

        liste = list()

        for item in result:
            
            model = MusteriAyrintiModel()
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.siparisno = item.SiparisNo 
            if item.YuklemeTarihi != None:
                model.yuklemetarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%Y-%m-%d")               


            
            urun_bedel = 0
            odeme = 0

            if item.UrunBedeli != None:
                urun_bedel = item.UrunBedeli
            if item.Odeme != None:
                odeme = item.Odeme

            model.toplam = urun_bedel + self.__noneControl(item.Iscilik)
            model.siparis_total = model.toplam
            
            model.kalan = self.__floatControlDecimal(model.toplam - self.__noneControl(odeme))
            model.kalan2 = model.toplam - odeme
            model.odenen_tutar = odeme
            model.iscilik = self.__noneControl(item.Iscilik)
            liste.append(model)

        return liste  


    
    