# coding=utf-8

from urlHandler import *
from dbHandler import *
import sys
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding('utf8')

def saveOrUpdateHouseInfo(houseInfoParam, houseInfoUpdateParam, housePriceParam, DB):
    if DB.checkHouseExist(houseInfoParam[0]):
        DB.updateHouseInfo(houseInfoUpdateParam[0], houseInfoUpdateParam[1], houseInfoUpdateParam[2],
                           houseInfoUpdateParam[3], houseInfoUpdateParam[4])
    else:
        DB.inserHouseInfo(houseInfoParam)
    DB.inserHousePrice(housePriceParam)


def saveCellInfo(cellParam, DB):
    if DB.checkCellExist(cellParam[0]):
        pass
    else:
        DB.insetCellInfo(cellParam)

def task(i):
    DB = dbHandler()
    houseIds = urlHandler.getHouseIdList(i)
    print "正在爬取第" + str(i) + "页数据...该页有:" + str(len(houseIds)) + '个房产信息'
    for houseId in houseIds:
        (houseInfoParam, houseInfoUpdateParam, housePriceParam, cellParam) = urlHandler.getAllHouseInfo(houseId)
        saveOrUpdateHouseInfo(houseInfoParam, houseInfoUpdateParam, housePriceParam, DB)
        saveCellInfo(cellParam, DB)
    DB.conn.close()

urlHandler = urlHandler()

# pool = threadpool.ThreadPool(3)
# requests = threadpool.makeRequests(task, range(1, 600))
# [pool.putRequest(req) for req in requests]
# pool.wait()

pool = Pool(processes=2)
for i in range(1, 600):
    pool.apply_async(task, (i, ))
pool.close()
pool.join()

# for i in range(137,600):
#     task(i)


