import urllib2
try:
    from bs4 import BeautifulSoup 
except ImportError:
    from BeautifulSoup import BeautifulSoup 

import sys

# ex 2017-Oct-23
targetDate=sys.argv[1]

class WSJ:
    def getAverageAnalystPrice(self, symbol):
        url = 'http://quotes.wsj.com/' + symbol + '/research-ratings'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        elements = soup.findAll('div', {"data-module-id":"7"})
        if len(elements) == 0:
            print 'WSJ no average price found for stock' + symbol
            return
        x = elements[0].find_all('tr')
        avgPrice = x[3].find_all('td')[1:]
        avgPrice[0].get_text()
        currPrice = x[4].find_all('td')[1:]
        currPrice[0].get_text()
        return "Average price=" + avgPrice[0].get_text().strip().encode('ascii', 'ignore') + " current price= " + currPrice[0].get_text().strip().encode('ascii', 'ignore')

class Zacks:
    def filterStocks(self, symbolList):
        base = 'https://www.zacks.com/stock/quote/'
        stockList = list()
        wsjZ = WSJ()
        for symbol in symbolList:
            url = base + symbol
            page  = urllib2.urlopen(url)
            soup = BeautifulSoup(page, "html.parser")
            elements = soup.findAll('section', {"id":"premium_research"})
            researchRating = soup.findAll('div', {'class': 'callout_box3 pad10'})
            if len(researchRating) == 0:
                print 'Rating not found for stock ' + symbol
                continue
            row =  researchRating[0].find_all('tr')
            if len(row) == 0:
                print 'some problem ' + symbol
                continue
            column = row[0].find_all('td')[0]
            rating = column.get_text().strip()
            if rating == "Strong Buy 1" or rating == "Buy 2" :
                stockList.append(symbol + " Zack Rank "+ rating + " Wsj Average price " + wsjZ.getAverageAnalystPrice(symbol))
        return stockList

class Nasdaq:
    def findAllSymbol(self):
        url = 'http://www.nasdaq.com/earnings/earnings-calendar.aspx?date=' + targetDate
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        elements = soup.findAll('table', {"id":"ECCompaniesTable"})
        myList = list()
        rows = elements[0].find_all('tr')
        for x in range(1, len(rows)):
            ref = rows[x].a['href'].encode('ascii','ignore')
            myList.append(ref.split("/")[-2].upper())
        return myList

nasdaq = Nasdaq()
oneDayList = nasdaq.findAllSymbol()
zacks = Zacks()
buyList = zacks.filterStocks(oneDayList)
for s in buyList:
    print s