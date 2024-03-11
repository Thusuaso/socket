from api.sql import *
from model.cost import *


class MaliyeZamanIslem:

    def __init__(self):

        self.data = SqlConnect().data


    def getYilListesi(self):

        result = self.data.getList(
            """
            select
            Year(s.YuklemeTarihi) as Yil
            from
            SiparislerTB s,MusterilerTB m,YeniTeklif_UlkeTB u,SiparisTeslimTurTB t
            where
            s.SiparisDurumID=3
            and m.Marketing='Mekmar'
            and m.UlkeId=u.Id
            and s.TeslimTurID=t.ID
            and s.MusteriID=m.ID
            and Year(s.YuklemeTarihi)>=2020
			group by Year(s.YuklemeTarihi)
			order by Year(s.YuklemeTarihi) desc
            """
        )

        liste = list()
        id = 1
        for item in result:

            model = MaliyetYilModel()
            model.id = id
            model.yil = item.Yil

            liste.append(model)

            id += 1

        schema = MaliyetYilSchema(many=True)

        return schema.dump(liste)

    def getAyListesi(self,yil):

        result = self.data.getStoreList(
            """
            select
            Month(s.YuklemeTarihi) as Ay
            from
            SiparislerTB s,MusterilerTB m,YeniTeklif_UlkeTB u,SiparisTeslimTurTB t
            where
            s.SiparisDurumID=3
            and m.Marketing='Mekmar'
            and m.UlkeId=u.Id
            and s.TeslimTurID=t.ID
            and s.MusteriID=m.ID
            and Year(s.YuklemeTarihi)>=?
			group by Month(s.YuklemeTarihi)
			order by Month(s.YuklemeTarihi) desc
            """,(yil)
        )

        liste = list()
        id = 1
        for item in result:

            model = MaliyetAyModel()
            model.id = id
            model.ay = item.Ay
            model.ay_str = self.__getAyStr(model.ay)

            liste.append(model)
            id += 1

        schema = MaliyetAySchema(many=True)

        return schema.dump(liste)

    def __getAyStr(self,ay):

        aylar = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']

        return aylar[ay-1]