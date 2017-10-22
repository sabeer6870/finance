import urllib2
try:
    from bs4 import BeautifulSoup 
except ImportError:
    from BeautifulSoup import BeautifulSoup 

import sys

#python stocks.py 2017-Oct-24 > Oct24.log
# ex 2017-Oct-23
targetDate=sys.argv[1]

class WSJ:
    def isCurrentPriceMoreThanAvgPrice(self, symbol):
        url = 'http://quotes.wsj.com/' + symbol + '/research-ratings'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        analystRatingTable = soup.findAll('table', {"class":"cr_dataTable"})
        if len(analystRatingTable) < 6:
            return False, '', 0, 0, 0, 0, 0
        rows = analystRatingTable[5].find_all('tr')
        if len(rows) < 7:
            return False, '', 0, 0, 0, 0, 0
        buyRating = rows[1].find_all('td')
        overWeightRating = rows[2].find_all('td')
        holdRating = rows[3].find_all('td')
        underweightRating = rows[4].find_all('td')
        sellRating = rows[5].find_all('td')
        overAllRating = rows[6].find_all('td')
        if len(buyRating) < 4 or len(overWeightRating)  < 4 or len(holdRating) < 4 or len(underweightRating) < 4 or len(sellRating) < 4:
            return False, '', 0, 0, 0, 0, 0
        numberOfBuy = buyRating[3].findAll('span', {'class': "data_data"})
        numberOfOverweight = overWeightRating[3].findAll('span', {'class': "data_data"})
        numberOfHold = holdRating[3].findAll('span', {'class': "data_data"})
        numberOfUnderWeight = underweightRating[3].findAll('span', {'class': "data_data"})
        numberOfSell = sellRating[3].findAll('span', {'class': "data_data"})
        r = overAllRating[3].findAll('div', {'class': "numValue-content"})[0].text.strip()
        if (r == 'Overweight' or r == 'Buy'):
            return True, r, numberOfBuy[0].text.strip(), numberOfOverweight[0].text.strip(), numberOfHold[0].text.strip(), numberOfUnderWeight[0].text.strip(), numberOfSell[0].text.strip()
        return False, r, numberOfBuy[0].text.strip(), numberOfOverweight[0].text.strip(), numberOfHold[0].text.strip(), numberOfUnderWeight[0].text.strip(), numberOfSell[0].text.strip()

class Zacks:
    def filterStocks(self, symbolList):
        base = 'https://www.zacks.com/stock/quote/'
        stockList = list()
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
            if rating == "Strong Buy 1" or rating == "Buy 2" or rating == "Hold 3":
                stockList.append(symbol + '-' + rating)
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
wsj = WSJ()
finalList = list()
#buyList = ['ANET-Buy']
for s in buyList:
    sn = s.split("-")[0]
    zr = s.split("-")[1]
    overall = ''
    b,r,nb,no,nh,nu,ns = wsj.isCurrentPriceMoreThanAvgPrice(sn)
    if r == '' or zr == '':
        continue
    rt = (s.split("-")[1] == 'Hold 3'and r == 'Hold')
    if b == True: #and rt == False:
        if zr == 'Strong Buy 1':
            overall  = overall + 'A' 
        elif zr == 'Buy 2':
            overall = overall + 'B'
        elif zr == 'Hold 3':
            overall = overall + 'C'
        if r == 'Buy':
            overall = overall + 'A'
        elif r == 'Overweight':
            overall = overall + 'B'
        elif r == 'Hold':
            overall = overall + 'C'
        print s + '-' + r + " overall= " + overall + " data=" + nb + "-" + no + "-" + nh + "-" + nu + "-" + ns