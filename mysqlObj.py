import mysql.connector
import json

class mysqlObj:
    def __init__(self) -> None:
        self.__args = self.__read_local_config()
        self.__connector = mysql.connector.connect(**self.__args)

    def __read_local_config(self):
        with open('mysql_config.json', "r") as file:
            config = json.load(file)
        return config
    
    def __del__(self) -> None:
        if self.__connector is None:
            return
        self.__connector.close()
    
    def close(self):
        if self.__connector is None:
            return
        self.__connector.close()

    def set_customized_stopwords(self,voc, user_id):
        try:
            if user_id is None or user_id == '':
                raise Exception('Invalid user_id')
            if(not self.__connector.is_connected()):
                self.__connector = mysql.connector.connect(**self.__args)

            cursor  = self.__connector.cursor()   
            if(not isinstance(voc,list)):
                voc = [voc]
            for element in voc:
                cursor.execute("INSERT INTO stopwordsdb.{0}_stopwords (vocabulary) VALUES (\'{1}\')".format(user_id, element))
        except Exception as ex:
            print(ex)
        finally:
            self.__connector.commit()
            cursor.close()
    def get_customized_stopwords(self,user_id):
        
        if user_id is None or user_id == '':
            raise Exception('Invalid user_id')
        if(not self.__connector.is_connected()):
            self.__connector = mysql.connector.connect(**self.__args)
        
        cursor = self.__connector.cursor()
        cursor.execute("SELECT vocabulary FROM stopwordsdb.{0}_stopwords".format(user_id))
        retrived_data = list(cursor)
        if(len(retrived_data) == 0):
            return []
        result = list(map(lambda x:x[0],retrived_data))
    
        self.__connector.commit()
        cursor.close()
        return result

def main():
    db = mysqlObj()
    db.set_customized_stopwords(['contain','Taiwan'],'jimmychangtw')
    result = db.get_customized_stopwords('jimmychangtw')
    print(result)
    db.close()
if(__name__ == '__main__'):
	main()