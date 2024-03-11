from marshmallow import Schema,fields,validate

class TedarikciFaturaSchema(Schema):
    id = fields.Int()
    link = fields.String()
    evrak_adi = fields.String()

class TedarikciFaturaModel:
    id = None
    link = ""
    evrak_adi = ""

class OzelMaliyetListeSchema(Schema):

    id = fields.Int()
    siparis_no = fields.String()
    marketing = fields.String()
    siparis_tarihi = fields.String()
    yukleme_tarihi = fields.String()
    musteri_adi = fields.String()
    ulke_adi = fields.String()
    teslim_sekli = fields.String()
    toplam_bedel = fields.Float()
    mekmar_alim = fields.Float()
    mekmoz_alim = fields.Float()
    dis_alim = fields.Float()
    nakliye = fields.Float()
    gumruk = fields.Float()
    ilaclama = fields.Float()
    liman = fields.Float()
    sigorta = fields.Float()
    lashing = fields.Float()
    booking = fields.Float()
    spazlet = fields.Float()
    sigorta_tutar_satis = fields.Float()
    detay_1 = fields.Float()
    detay_2 = fields.Float()
    detay_3 = fields.Float()
    navlun = fields.Float()
    operasyon = fields.String()
    siparisci = fields.String()
    faturatur = fields.String()
    
    diger_masraflar = fields.Float()
    pazarlama = fields.Float()
    banka_masrafi = fields.Float()
    kurye_masrafi = fields.Float()
    masraf_toplam = fields.Float()
    kar_zarar = fields.Float()
    odeme_tarihi = fields.String()
    kar_zarar_tl = fields.Float()
    kar_zarar_tl_yuzdesi = fields.Float()
    doviz_kur = fields.Float()
    Kur = fields.Float()
    nakliye_evrak = fields.String()
    gumruk_evrak = fields.String()
    ilaclama_evrak = fields.String()
    liman_evrak = fields.String()
    sigorta_evrak = fields.String()
    navlun_evrak = fields.String()
    lashing_evrak = fields.String()
    booking_evrak = fields.String()
    spazlet_evrak = fields.String()
    mekmar_alim_evrak = fields.Nested(TedarikciFaturaSchema(many=True))
    mekmar_alim_evrak_sayisi = fields.Int()
    mekmoz_alim_evrak = fields.Nested(TedarikciFaturaSchema(many=True))
    mekmoz_alim_evrak_sayisi = fields.Int()
    dis_alim_evrak = fields.Nested(TedarikciFaturaSchema(many=True))
    dis_alim_evrak_sayisi = fields.Int()
    dis_alim_tedarikci =  fields.Nested(TedarikciFaturaSchema(many=True))
    dis_alim_tedarikci_sayisi = fields.Int()
    tedarikci_sayisi = fields.Int()
    satis_faturasi = fields.String() #toplam bedel
    evrak_id = fields.Int()
    tur_id = fields.Int()
    navlun_kontrol = fields.Boolean()
    navlun_satis = fields.Float()
    dis_alim_fatura_sayisi = fields.Int()
    ozel_iscilik = fields.Int()
    ozel_iscilik_evrak = fields.Nested(TedarikciFaturaSchema(many=True))
    tedarikci_sayisi_evrak = fields.Nested(TedarikciFaturaSchema(many=True))
    ozel_iscilik_sayisi = fields.Int()
    odenen_toplam_tutar = fields.Float()
    dosya_kapanma_date = fields.String()
    mekus_masraf = fields.Float()
    mekus_id = fields.Int()
    sigorta_id = fields.Boolean()
    odenen_try_tutar = fields.Float()
    odenen_usd_tutar = fields.Float()
    ortalama_kur = fields.Float()
    yukleme_year = fields.Int()
    yukleme_month = fields.Int()
    alisFiyatiKontrol = fields.String()
    yukleme_day = fields.String()
    isciliktedarikcimekmer = fields.Boolean()
    isciliktedarikcimekmoz = fields.Boolean()
class OzelMaliyetListeModel:

    id = None
    siparis_no = "" 
    marketing = ""
    siparis_tarihi = ""
    yukleme_tarihi = ""
    musteri_adi = ""
    ulke_adi = ""
    teslim_sekli = ""
    toplam_bedel = 0 # ürün bedeli + navlun + müşteriden tahsil edilen extra gelirler
    mekmar_alim = 0
    mekmoz_alim = 0
    dis_alim = 0
    nakliye = 0
    gumruk = 0
    ilaclama = 0
    liman = 0
    sigorta = 0
    lashing = 0
    booking = 0
    spazlet = 0
    sigorta_tutar_satis = 0
    Kur = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    navlun = 0
    diger_masraflar = 0
    pazarlama = 0 #komisyon
    banka_masrafi = 0
    kurye_masrafi = 0
    masraf_toplam = 0
    kar_zarar = 0
    odeme_tarihi = ""
    doviz_kur = 0
    kar_zarar_tl = 0
    kar_zarar_tl_yuzdesi=0
    nakliye_evrak = ""
    operasyon = ""
    siparisci = ""
    faturatur = ""
    alisFiyatiKontrol = ""
    sigorta_evrak = ""
    gumruk_evrak = ""
    ilaclama_evrak = ""
    liman_evrak = ""
    navlun_evrak = ""
    lashing_evrak = ""
    booking_evrak = ""
    spazlet_evrak = ""
    mekmar_alim_evrak = list()
    mekmar_alim_evrak_sayisi = 0
    mekmoz_alim_evrak = list()
    dis_alim_evrak = list()
    dis_alim_tedarikci = list()
    dis_alim_tedarikci_sayisi = 0
    tedarikci_sayisi = 0
    tedarikci_sayisi_evrak = list()
    satis_faturasi = ""
    evrak_id = None
    tur_id = None
    navlun_kontrol = True
    sigorta_id = True
    navlun_satis = 0
    dis_alim_fatura_sayisi = 0
    dis_alim_fatura_list = list()
    ozel_iscilik = 0 
    odenen_toplam_tutar = 0
    dosya_kapanma_date = ""
    ozel_iscilik_evrak = ""
    mekus_masraf = 0
    mekus_id = None 
    odenen_try_tutar = 0
    odenen_usd_tutar = 0
    ortalama_kur = 0
    yukleme_year = 0
    yukleme_month = 0
    yukleme_day = 0
    isciliktedarikcimekmer = False
    isciliktedarikcimekmoz = False



class OzelMaliyetListeKarSchema(Schema):
    musteri_id = fields.Int()
    musteri_adi = fields.String()
    siparis_no = fields.String()
    navlun_satis = fields.Float()
    detay_1 = fields.Float()
    detay_2 = fields.Float()
    detay_3 = fields.Float()
    navlun_alis = fields.Float()
    detay_alis_1 = fields.Float()
    detay_alis_2 = fields.Float()
    detay_alis_3 = fields.Float()
    sigorta_tutar_satis = fields.Float()
    mekus_masraf = fields.Float()
    toplam_bedel = fields.Float()
    satis_toplami = fields.Float()
    alis_toplami = fields.Float()
    banka_masrafi = fields.Float()
    odenen_usd_tutar = fields.Float()
    odenen_try_tutar = fields.Float()
    ortalama_kur = fields.Float()
    fatura_masraflari = fields.Float()
    masraf_toplam = fields.Float()
    kar_zarar = fields.Float()
    kar_zarar_tl = fields.Float()
    kar_zarar_orani = fields.Float()
    yukleme_yil = fields.String()
    yukleme_ay = fields.String()
    yukleme_gun = fields.String()
    masraf_toplam_tl = fields.Float()
    komisyon = fields.Float()
    evrak_gideri = fields.Float()
    iscilik_masrafi = fields.Float()
    banka_masrafi = fields.Float()
    sigorta_alis = fields.Float()
    kalan_bedel = fields.Float()
    yukleme_tarihi = fields.String()
class OzelMaliyetListeKarModel:
    musteri_id = 0
    musteri_adi = ""
    siparis_no = ""
    navlun_satis = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    sigorta_tutar_satis = 0
    mekus_masraf = 0
    toplam_bedel = 0
    satis_toplami = 0
    alis_toplami = 0
    banka_masrafi = 0
    odenen_usd_tutar = 0
    odenen_try_tutar = 0
    ortalama_kur = 0
    fatura_masraflari = 0
    masraf_toplam = 0
    masraf_toplam_tl = 0
    kar_zarar = 0
    kar_zarar_tl = 0
    kar_zarar_orani = 0
    yukleme_yil = ""
    yukleme_ay = ""
    yukleme_gun = ""
    navlun_alis = 0
    detay_alis_1 = 0
    detay_alis_2 = 0
    detay_alis_3 = 0
    komisyon = 0
    evrak_gideri = 0
    iscilik_masrafi = 0
    banka_masrafi = 0
    sigorta_alis = 0
    kalan_bedel = 0
    yukleme_tarihi = 0
    
    
class TedarikciFaturaSchema(Schema):
    id = fields.Int()
    link = fields.String()
    evrak_adi = fields.String()

class TedarikciFaturaModel:
    id = None
    link = ""
    evrak_adi = ""
    
class OzelMaliyetAyrintiSchema(Schema):

    id = fields.Int()
    siparis_no = fields.String()
    invoiced = fields.Float()
    mekmer_alim = fields.Float()
    mek_moz_alim = fields.Float()
    dis_alim  = fields.Float()
    
    nakliye = fields.Float()
    gumruk = fields.Float()
    ilaclama = fields.Float()
    liman = fields.Float()
    sigorta = fields.Float()
    navlun_alis = fields.Float()
    detay_1 = fields.Float()
    detay_2 = fields.Float()
    detay_3 = fields.Float()
    mekus_masraf = fields.Float()
    komisyon = fields.Float()
    ozel_iscilik = fields.Float()
    banka_masrafi = fields.Float()
    kurye = fields.Float()
    total_in = fields.Float()
    navlun = fields.Float()
    alisFiyatiControl = fields.Boolean()
    kur = fields.Float()
    
  

class OzelMaliyetAyrintiModel:

    id = None
    siparis_no = "" 
   
    invoiced = 0
    mekmer_alim = 0
    mek_moz_alim = 0
    dis_alim  = 0
    nakliye = 0
   
    gumruk = 0
    ilaclama = 0
    sigorta = 0
    liman = 0
    navlun_alis = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    mekus_masraf = 0
    komisyon = 0
    ozel_iscilik = 0
    banka_masrafi = 0
    kurye = 0
    total_in = 0
    alisFiyatiControl = False
    kur = 0
    
class BankaAyrintiSchema(Schema):

    id = fields.Int()
    siparis_no = fields.String()
    tutar = fields.Float() 
    tutartl = fields.Float()
    kur= fields.Float()
    masraf = fields.Float()
    tarih = fields.String()
   
    
  

class BankaAyrintiModel:

    id = None
    siparis_no = ""
    tutar = 0
    tutartl = 0
    kur = 0
    masraf = 0
    tarih = ""
    

class EvrakSiparisListeSchema(Schema):
    id = fields.Int() 
    siparisno = fields.String()
    musteriid = fields.Int()
   
    mail = fields.String()
    musteriAdi = fields.String()
    odeme = fields.String()
    teslim = fields.String()
    ulke = fields.String()
    eta = fields.String()
    KonteynerNo = fields.String()
    line = fields.String()
    navlunAlis = fields.Float()
    navlunSatis = fields.Float()

class EvrakSiparisListeModel:

    id = None 
    siparisno = ""
    musteriid = None 
    mail = ""
    musteriAdi =""
    odeme = ""
    teslim = ""
    ulke = ""
    eta = ""
    KonteynerNo = ""
    line = ""
    navlunAlis = 0
    navlunSatis = 0

class EvrakListeSchema(Schema):
    Faturaid = fields.Int() 
    faturaadi = fields.String()
    renk = fields.String()
    

class EvrakListeModel:

    Faturaid = None 
    faturaadi = ""
    renk = ""

class FaturaListeSchema(Schema):
    id = fields.Int() 
    faturaId = fields.Int()
    yuklemeTarihi =fields.DateTime()
    adi = fields.String()
    Draft = fields.String()
    kullanici = fields.String()
    faturano = fields.String()
    yeniID = fields.String()
    yeniEvrakAdi = fields.String()
    durum = fields.Int()
    olmayan_durum = fields.String()
    evrakadi = fields.String()
    tedarikciId = fields.Int()
    siparisNo = fields.String()

class FaturaListeModel:

    id = None
    faturaId = 0
    yuklemeTarihi = ""  
    adi = ""  
    Draft =""
    kullanici = ""
    faturano = ""
    yeniID = ""
    yeniEvrakAdi = ""
    durum = 0
    olmayan_durum = ""
    tedarikciId =0
    evrakadi=""
    siparisNo = ""

class FaturaKayitSchema(Schema):
     id = fields.Int() 
     kullaniciAdi = fields.String()
     siparisno = fields.String()


class FaturaKayitModel:

    id = None 
    kullaniciAdi = ""
    siparisno = ""  

    
class TedarikciSchema(Schema):

     ID = fields.Int() 
     tedarikci = fields.String()
     siparisno = fields.String()


class TedarikciModel:

    ID = None
    tedarikci = ""
    siparisno = ""      
   

