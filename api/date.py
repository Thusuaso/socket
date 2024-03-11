import datetime

class TarihIslemler:

    def getDate(self,date):
        try:
            year,month,_date = str(date).split('-')

            return datetime.datetime(int(year),int(month),int(_date))
        except:
            return None
