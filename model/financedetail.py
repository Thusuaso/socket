from marshmallow import Schema,fields

class FinanceDetailSchema(Schema):
    customer_id = fields.Int()
    po = fields.String()
    cost = fields.Float()
    paid = fields.Float()
    balance = fields.Float()
    status = fields.String()
    advanced_payment = fields.Float()
    product_date = fields.String()
    forwarding_date = fields.String()
    maya_control = fields.Boolean()
    paid_date = fields.List(fields.Dict(keys=fields.String(),values=fields.String()))
class FinanceDetailModel:
    customer_id = 0
    po = ""
    cost = 0
    paid = 0
    balance = 0
    status = ""
    advanced_payment = 0
    product_date = ""
    forwarding_date = ""
    maya_control = False
    paid_date = []
class ByDatePaidsSchema(Schema):
    id = 0
    date = fields.String()
    paid = fields.Float()
    
class ByDatePaidsModel:
    id = 0
    date = ""
    paid = 0
class VadeAnaListeSchema(Schema):

    firmaAdi = fields.String()
    tutar = fields.Float()
    siparis_no = fields.String()
    vade_tarih = fields.String()
  

class VadeAnaListeModel:
    
    firmaAdi = ""
    tutar = 0
    siparis_no = ""
    vade_tarih = ""

class MusteriOdemeSecimSchema(Schema):
    id = fields.Int()
    siparisno= fields.String()
    tutar = fields.Float()
    aciklama = fields.String()
    masraf = fields.Float()
    faturatur = fields.String()
    sira = fields.Int()
    kur = fields.Float()
    tarih = fields.String()
    musteri_id = fields.Int()
    musteriadi = fields.String()

class MusteriOdemeSecimModel:
    id = None
    siparisno = ""
    tutar = 0
    aciklama = ""
    masraf = 0 
    faturatur = ""
    sira = 0
    kur = 0
    tarih = ""
    musteri_id = 0
    musteriadi = ""

class MusteriAyrintiSchema(Schema):

    id = fields.Int()
    musteriadi = fields.String()
    musteri_id = fields.Int()
    siparisno = fields.String()
    yuklemetarihi = fields.String()
    tip = fields.String()
    toplam = fields.Float()
    kalan = fields.Float()
    vade = fields.String()
    pesinat = fields.Float()
    siparis_total = fields.Float()
    odenen_tutar = fields.Float()
    tahmini_eta = fields.String()
    kalan2 = fields.Float()
class MusteriAyrintiModel:
    id = None
    musteriadi = ""
    musteri_id = None
    siparisno = ""
    yuklemetarihi = ""
    tip = ""
    toplam = 0
    kalan = 0
    vade = ""
    pesinat = 0
    siparis_total = 0
    odenen_tutar = 0
    tahmini_eta = ""
    kalan2 = 0
    
class ByCustomersPoSchema(Schema):
    id = fields.Int()
    siparisNo = fields.String()

class ByCustomersPoModel:
    id = 0
    siparisNo = ""
    
class MusteriOdemeSchema(Schema):
    id = fields.Int()
    tarih = fields.String()
    tutar = fields.Float()


class MusteriOdemeModel:
    id = None 
    tarih = ""
    tutar = 0


