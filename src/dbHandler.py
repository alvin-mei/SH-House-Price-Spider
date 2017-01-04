import MySQLdb
import traceback

class dbHandler:
    host = '127.0.0.1'
    user = 'root'
    password = ''
    dbName = 'lianjia'
    port = 3306

    conn = None
    cursor = None
    def __init__(self):
        self.conn = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.dbName,
            port=self.port)
        self.cursor = self.conn.cursor()

    def inserHouseInfo(self, params):
        vStr = []
        for param in params:
            vStr.append("'" + MySQLdb.escape_string(str(param)) + "'")
        values = ','.join(vStr)
        try:
            self.cursor.execute("""
              INSERT INTO houseInfo(houseId, cellId, currentPrice, perSquarePrice, downPayment, moneyMonth, area, room, year)
              VALUES(%s)""" %values)
            result = self.conn.insert_id()
            self.conn.commit()
            return result
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return 0

    def inserHousePrice(self, params):
        vStr = []
        for param in params:
            vStr.append("'" + MySQLdb.escape_string(str(param)) + "'")
        values = ','.join(vStr)
        try:
            self.cursor.execute("""
              INSERT INTO housePrice(houseId, cellId, currentPrice, perSquarePrice)
              VALUES(%s)""" %values)
            result = self.conn.insert_id()
            self.conn.commit()
            return result
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return 0

    def insetCellInfo(self, params):
        vStr = []
        for param in params:
            vStr.append("'" + MySQLdb.escape_string(str(param)) + "'")
        values = ','.join(vStr)
        print values
        try:
            self.cursor.execute("""
                        INSERT INTO cellInfo(cellId, name, address, regionId, url)
                        VALUES(%s)""" % values)
            result = self.conn.insert_id()
            self.conn.commit()
            return result
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return 0

    def updateHouseInfo(self, id, currentPrice, perSquarePrice, downPayment, moneyMonth):
        try:
            result = self.cursor.execute("""
              UPDATE houseInfo
              SET currentPrice = %d, perSquarePrice = %d, downPayment = %d, moneyMonth = %d
              WHERE houseId = %d""" %(int(currentPrice), int(perSquarePrice), int(downPayment), int(moneyMonth), int(id)))
            self.conn.commit()
            return result
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return 0



    def checkHouseExist(self, houseId):
        try:
            self.cursor.execute(
                """SELECT COUNT(1) FROM houseInfo
                    WHERE houseId = %d
                    AND status = 0""" %int(houseId))
            count = self.cursor.fetchone()[0]
            if count > 0:
                return True
            else:
                return False
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return False

    def checkCellExist(self, cellId):
        try:
            self.cursor.execute(
                """SELECT COUNT(1) FROM cellInfo
                    WHERE cellId = %d
                    AND status = 0""" % int(cellId)
            )
            count = self.cursor.fetchone()[0]
            if count > 0:
                return True
            else:
                return False
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr
            return False

