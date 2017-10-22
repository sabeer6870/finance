import urllib2
try:
    from bs4 import BeautifulSoup 
except ImportError:
    from BeautifulSoup import BeautifulSoup 

import sys
weekStart=sys.argv[1]
weekEnd=sys.argv[2]
day=sys.argv[3]

class WSJ:
    def getAverageAnalystPrice(self, symbol):
        url = 'http://quotes.wsj.com/' + symbol + '/research-ratings'
        page = urllib2.urlopen('http://quotes.wsj.com/WMT/research-ratings')
        soup = BeautifulSoup(page, "html.parser")
        elements = soup.findAll('div', {"data-module-id":"7"})
        if len(elements) == 0:
            print 'WSJ no average price found for stock' + symbol
            return
        x = elements[0].find_all('tr')
        y = x[3].find_all('td')[1:]
        y[0].get_text()
        return y[0].get_text().strip().encode('ascii', 'ignore')

class Yahoo:
    def getStocksListNextSevenDays(self):
        base = 'https://finance.yahoo.com/calendar/earnings?from=' + weekStart + '&to=' + weekEnd + '&day=' + day
        symbolList = list()
        sum = 0;
        offset = 0
        while offset < 400:
            url = base + '&offset=' + str(offset) + '&size=100'
            print url
            page = urllib2.urlopen(base)
            soup = BeautifulSoup(page, "html.parser")
            elements = soup.findAll('div', {"data-reactid":"15"})
            print len(elements)
            if len(elements) < 3:
                print 'Yahoo Earning returned list of size less than 2, i.e no earnings found'
                break 
            sum = sum + len(elements[2].find_all('tr'))
            x = elements[2].find_all('tr')
            i = 0
            symbolList = list()
            for row in x[0].find_all('tr'):
                if i == 0:
                    i += 1
                    continue;
                symbolList.append(row.a['data-symbol'].encode('ascii','ignore'))
            offset = offset + 100
        print sum    
        return symbolList

class Zacks:
    def filterStocks(self, symbolList):
        print symbolList
        base = 'https://www.zacks.com/stock/quote/'
        stockList = list()
        for symbol in symbolList:
            url = base + symbol
            page  = urllib2.urlopen(url)
            soup = BeautifulSoup(page, "html.parser")
            elements = soup.findAll('section', {"id":"premium_research"})
            researchRating = soup.findAll('div', {'class': 'callout_box3 pad10'})
            if researchRating == 0:
                print 'Rating not founf for stock ' + symbol
                continue
            row =  researchRating[0].find_all('tr')
            column = row[0].find_all('td')[0]
            rating = column.get_text().strip()
            if rating == "Strong Buy 1":
                stockList.append(symbol)
            elif rating == "Buy 2":
                stockList.append(symbol)
        return stockList

wsj = WSJ()
wsj.getAverageAnalystPrice('WMT')
yahoo = Yahoo()
sList = yahoo.getStocksListNextSevenDays()
zacks = Zacks()
print zacks.filterStocks(['WMT', 'HUBS', 'MXIM', 'JRONY'])