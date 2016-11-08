# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

# DB accessor
class Dbaccessor:

    def __init__(self):
        try:
            # get database connection
            self.connector = mysql.connector.connect(host="localhost", db="ssxz", user="s_user1", passwd="Qwer1234@", charset="utf8") 
        except mysql.connector.Error as e:
            print("can't get db connection: {}".format(e))
      
    # insert a record into resourceinfo
    def insertResourceInfo(self, machineid, aeraid, capacity, status):
        try:
            cursor = self.connector.cursor() 
            cursor.execute("insert into resourceinfo values(%s, %s, %s, %s)", (machineid, aeraid, capacity, status))
            cursor.close()
        except mysql.connector.Error as e:
            print("insert error:" + e.errno + ":" + e.msg)
      
    # get resource info
    def selectResourceInfo(self, machineid, aeraid):
        try:
            cursor = self.connector.cursor() 
            cursor.execute("select status from resourceinfo where machineid=%s and aeraid=%s", (machineid, aeraid))
            result = cursor.fetchall()
            status = result[0][0]
            cursor.close()
        except mysql.connector.Error as e:
            print("select error:" + e.errno + ":" + e.msg)
            
        return status

    # update resource info
    def updateResourceInfo(self, machineid, aeraid, status):
        try:
            cursor = self.connector.cursor() 
            cursor.execute("update resourceinfo set status=%s where machineid=%s and aeraid=%s", (status, machineid, aeraid)) 
            cursor.close()
        except mysql.connector.Error as e:
            print("update error:" + e.errno + ":" + e.msg)

    # delete resource info
    def deleteResourceInfo(self, machineid, aeraid):
        try:
            cursor = self.connector.cursor() 
            cursor.execute("delete from resourceinfo where machineid=%s and aeraid=%s", (machineid, aeraid))
            cursor.close()
        except mysql.connector.Error as e:
            print("update error:" + e.errno + ":" + e.msg)
        
    # commit
    def commit(self):
        self.connector.commit()

    # close connection
    def closeConnection(self):
        self.connector.close()

if __name__ == "__main__":
    test=Dbaccessor()
    a=test.selectResourceInfo(1,1)
    print("--status--")
    print(a)
    test.insertResourceInfo(2,1,1000,1)
    test.updateResourceInfo(2,1,2)
    test.deleteResourceInfo(2,1)
    test.commit()
    test.closeConnection()

