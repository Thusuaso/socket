import pyodbc


class SqlIslem:
    def __init__(self):
        
        self.con_str = 'Driver={ODBC Driver 17 for Sql Server};Server=94.73.151.2;Database=Yeni_Mekmar_DB;Uid=userEC52E044DE;Pwd=POlb33D8PQlo68S'
        #self.con_str = 'Driver={Sql Server};Server=94.73.151.2;Database=Yeni_Mekmar_DB;Uid=userEC52E044DE;Pwd=BXrz21F7'
        
        
        
    def getList(self,sorgu):
        self.data = pyodbc.connect(self.con_str)
        self.cursor = self.data.cursor()
        self.cursor.execute(sorgu)
        result = self.cursor.fetchall()
        self.data.close()
        return result

    def getStoreList(self,sorgu,parametre):
        self.data = pyodbc.connect(self.con_str)
        self.cursor = self.data.cursor()
        self.cursor.execute(sorgu,parametre)
        result = self.cursor.fetchall()
        self.data.close()
        return result

    def update_insert(self,sorgu,parametre):
        self.data = pyodbc.connect(self.con_str)
        self.cursor = self.data.cursor()
        self.cursor.execute(sorgu,parametre)
        self.data.commit()
        self.data.close()

    
    def close(self):
        
        self.data.close()
        
    def save(self):
        self.data.commit()
        

class SqlConnect:
    def __init__(self):
        self.data = SqlIslem()