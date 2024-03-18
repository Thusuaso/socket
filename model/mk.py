from marshmallow import Schema,fields
class PoBazindaYillikSchema(Schema):
    po = fields.String()
    fob = fields.Float()
    ddp = fields.Float()
    teslim = fields.String()
    firma = fields.String()
    tarih = fields.String()
class PoBazindaYillikModel:
    po = ""
    fob = 0
    ddp = 0
    teslim = ""
    firma = ""
    tarih = ""
    
class MusteriBazindaUretimModel:
    musteriAdi = ""
    marketing = ""
    ulkeAdi = ""
    toplam = 0
    toplamCfr = 0


class MusteriBazindaUretimSchema(Schema):
    musteriAdi = fields.String()
    marketing = fields.String()
    ulkeAdi = fields.String()
    toplam = fields.Float()
    toplamCfr = fields.Float()
    
class MarketingSchema(Schema):
    marketing = fields.String()
    fobToplam = fields.Float()
    cfrToplam = fields.Float()
    
class MarketingModel:
    marketing = ""
    fobToplam = 0
    cfrToplam = 0
    
class MarketingAyrintiSchema(Schema):
    musteri = fields.String()
    marketing = fields.String()
    toplamFob = fields.Float()
    toplamCfr = fields.Float()
    
class MarketingAyrintiModel:
    musteri = ""
    marketing = ""
    toplamFob = 0
    toplamCfr = 0
    
class MkRaporlarSevkSipSchema(Schema):
    po = fields.String()
    tarih = fields.String()
    siparisfob = fields.Float()
    siparisddp = fields.Float()
    yuklenenfob = fields.Float()
    yuklenenddp = fields.Float()
    teslimtur = fields.String()
    musteriadi = fields.String()
    siparistarihi = fields.String()
    yuklemetarihi = fields.String()
    total = fields.Float()
class MkRaporlarSevkSipModel:
    po = ""
    tarih = ""
    fob = 0
    ddp = 0
    siparisfob = 0
    siparisddp = 0 
    yuklenenfob = 0
    yuklenenddp = 0
    teslimtur = ""
    musteriadi = ""
    siparistarihi = ""
    yuklemetarihi = ""
    total = 0
    
class KullaniciSchema(Schema):

     
     musteri_id = fields.Int()
     musteri = fields.String()
     ulkeAdi = fields.String()
     
     sonSiparisTarihi = fields.String()
     logo = fields.String()
     BuYil = fields.Float()
     GecenYil = fields.Float()
     OncekiYil = fields.Float()
     OnDokuzYili = fields.Float()
     OnSekizYili = fields.Float()
     OnYediYili = fields.Float()
     OnAltiYili = fields.Float()
     OnBesYili = fields.Float()
     OnDortYili = fields.Float()
     OnUcYili = fields.Float()
     OnUcYiliOncesi = fields.Float()
     Toplam = fields.Float()
     marketing = fields.String()
     oncelik = fields.String()
     temsilci = fields.String()
     BuYilUretim = fields.Float()
     BuYilSevkiyat = fields.Float()
   

    
class KullaniciModel:

    
    musteri_id = 0
    musteri = ""
    ulkeAdi = ""
    logo = ""
    BuYil = 0
    GecenYil = 0
    OncekiYil = 0
    sonSiparisTarihi = ""
    OnDokuzYili = 0
    OnSekizYili = 0
    OnYediYili = 0
    OnAltiYili = 0
    OnBesYili = 0
    OnDortYili = 0
    OnUcYili = 0
    OnUcYiliOncesi=0
    Toplam = 0 
    marketing = ""
    oncelik = ""
    temsilci = ""
    BuYilUretim = 0
    BuYilSevkiyat = 0
   
   
   
class MaliyetKullaniciModel:
    id = 0
    name = ""
    
class MaliyetKullaniciSchema(Schema):
    id = fields.Int()
    name = fields.String()