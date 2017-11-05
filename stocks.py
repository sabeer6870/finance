import urllib2
try:
    from bs4 import BeautifulSoup 
except ImportError:
    from BeautifulSoup import BeautifulSoup 

import sys

#python stocks.py 2017-Oct-24 > Oct24.log
# ex 2017-Oct-23
targetDate=sys.argv[1]
columSeparator = ' | '
Length = 15
TotalWidth = 33
Breaker =  "|"+"- " * TotalWidth + " |"

class WSJ:
    def ratingFromWsj(self, symbol):
        url = 'http://quotes.wsj.com/' + symbol + '/research-ratings'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        analystRatingTable = soup.findAll('table', {"class":"cr_dataTable"})
        if len(analystRatingTable) < 6:
            return 'NA', '0-0-0-0-0', 0
        rows = analystRatingTable[5].find_all('tr')
        if len(rows) < 7:
            return 'NA', '0-0-0-0-0', 0
        buyRating = rows[1].find_all('td')
        overWeightRating = rows[2].find_all('td')
        holdRating = rows[3].find_all('td')
        underweightRating = rows[4].find_all('td')
        sellRating = rows[5].find_all('td')
        overAllRating = rows[6].find_all('td')
        if len(buyRating) < 4 or len(overWeightRating)  < 4 or len(holdRating) < 4 or len(underweightRating) < 4 or len(sellRating) < 4:
            return 'NA', '0-0-0-0-0', 0
        numberOfBuy = buyRating[3].findAll('span', {'class': "data_data"})
        numberOfOverweight = overWeightRating[3].findAll('span', {'class': "data_data"})
        numberOfHold = holdRating[3].findAll('span', {'class': "data_data"})
        numberOfUnderWeight = underweightRating[3].findAll('span', {'class': "data_data"})
        numberOfSell = sellRating[3].findAll('span', {'class': "data_data"})
        r = overAllRating[3].findAll('div', {'class': "numValue-content"})[0].text.strip()
        summary = numberOfBuy[0].text.strip()+"-"+ numberOfOverweight[0].text.strip()+"-"+ numberOfHold[0].text.strip()+"-"+ numberOfUnderWeight[0].text.strip()+"-"+ numberOfSell[0].text.strip()
        totalNumberOfRating = int(numberOfBuy[0].text.strip()) + int(numberOfOverweight[0].text.strip()) + int(numberOfHold[0].text.strip()) + int(numberOfUnderWeight[0].text.strip()) + int(numberOfSell[0].text.strip())
        if (r == 'Overweight' or r == 'Buy' or r == 'Hold'):
            return r, summary, totalNumberOfRating
        return 'NA', summary, totalNumberOfRating

class Zacks:
    def ratingFromZacks(self, symbol):
        base = 'https://www.zacks.com/stock/quote/'
        url = base + symbol
        page  = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        elements = soup.findAll('section', {"id":"premium_research"})
        researchRating = soup.findAll('div', {'class': 'callout_box3 pad10'})
        if len(researchRating) == 0:
            print 'Rating not found for stock ' + symbol
            return 'NA'
        row =  researchRating[0].find_all('tr')
        if len(row) == 0:
            print 'some problem ' + symbol
            return 'NA'
        column = row[0].find_all('td')[0]
        rating = column.get_text().strip()
        if rating == 'Strong Buy 1' or rating == 'Buy 2' or rating == 'Hold 3':
            return rating
        return 'NA' 

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
print len(oneDayList)
#oneDayList = ['FANG', 'COHR', 'RSPP']
zacks = Zacks()
wsj = WSJ()

print Breaker
print columSeparator.join(['|Symbol'.ljust(Length),'Zacks'.ljust(Length), 'WSJ'.ljust(Length), 'WSJ All Rating'.ljust(Length-1) + "|"])
print Breaker
for item in oneDayList:
    singleList = list()
    zRating = zacks.ratingFromZacks(item)
    if zRating != 'NA':
        wsjRating,summary, totalNumberOfRating = wsj.ratingFromWsj(item)
        bothHold = (wsjRating == 'Hold' and zRating == 'Hold 3')
        noneHold = (wsjRating != 'Hold' and zRating != 'Hold 3')
        if wsjRating != 'NA' and totalNumberOfRating > 5 and bothHold == False:
            singleList.append("|" + item.ljust(Length-1))
            singleList.append(zRating.encode('ascii','ignore').ljust(Length))
            singleList.append(wsjRating.encode('ascii','ignore').ljust(Length))
            singleList.append(summary.encode('ascii','ignore').ljust(Length-1)+ "|")
            print columSeparator.join(singleList)
            print Breaker