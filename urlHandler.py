import urllib2
from bs4 import BeautifulSoup
import re

class urlHandler:
    BASE_WEB_URL = 'http://sh.lianjia.com/ershoufang/pudongxinqu/'
    BASE_APP_URL = 'http://m.sh.lianjia.com/ershoufang/sh4200078.html'

    def getHouseIdList(self):
        houseIds = set()
        request = urllib2.Request(self.BASE_WEB_URL)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all('a', key=re.compile('sh\d+'))
        for i in items:
            houseId = i.get('key')
            houseIds.add(houseId)
        return houseIds

    def getHouseInfo(self):
        request = urllib2.Request(self.BASE_APP_URL)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        print soup