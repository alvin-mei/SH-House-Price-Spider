import urllib2
from bs4 import BeautifulSoup
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class urlHandler:
    BASE_WEB_URL = 'http://sh.lianjia.com/ershoufang/pudongxinqu'
    BASE_APP_URL = 'http://m.sh.lianjia.com/ershoufang'

    def getHouseIdList(self, page):
        url = self.BASE_WEB_URL + '/d' + str(page)
        houseIds = set()
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all('a', key=re.compile('sh\d+'))
        for i in items:
            houseId = i.get('key')
            houseIds.add(houseId)
        return houseIds

    def getAllHouseInfo(self, houseId):
        url = self.BASE_APP_URL + '/' + str(houseId) + '.html'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")

        houseId = soup.find('input', id='houseSellId')['value']
        currentPrice = soup.find('input', id='js_wx_price')['value']
        area = soup.find('input', id='js_wx_acreage')['value']

        allOrange = soup.find_all('p', class_='c-orange')
        room = allOrange[1].string

        allValue = soup.find_all('span', class_='d-value')
        perSquarePrice = 0
        if allValue != None:
            perSquarePrice = "".join(re.findall('\d+', allValue[0].string.strip()))
        downPayment = re.findall('\d+', allValue[1].string.strip())[0]
        moneyMonth = "".join(re.findall('\d+', allValue[2].string.strip()))
        year = allValue[7].string.strip()
        url = soup.find('li', class_='linkline').a.get('href')
        cellId = re.findall('\d+', url)[0]
        cellName = allValue[9].string.strip()
        cellAddress = ''
        cellAddressSoup = soup.find('p', class_='d-value')
        if cellAddressSoup != None:
            cellAddress = cellAddressSoup.string

        houseInfoParam = [houseId, cellId, currentPrice, perSquarePrice, downPayment, moneyMonth, area, room, year]
        houseInfoUpdateParam = [houseId, currentPrice, perSquarePrice, downPayment, moneyMonth]
        housePriceParam = [houseId, cellId, downPayment, moneyMonth]
        cellParam = [cellId, cellName, cellAddress, 1, url]

        return (houseInfoParam, houseInfoUpdateParam, housePriceParam, cellParam)