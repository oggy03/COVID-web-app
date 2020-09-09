import requests
from bs4 import BeautifulSoup

def getHeadlines():
    response = requests.get('http://www.bbc.co.uk/news/coronavirus')
    doc = BeautifulSoup(response.text, 'lxml')
    links = doc.find_all('a', {'class': 'gs-c-promo-heading'})
    headlines = []
    print("")
    for link in links[:10]:
        a = link.text[:8]
        if a != "LiveLive" and [link.text,"https://www.bbc.co.uk"+link["href"]] not in headlines:
            headlines.append([link.text,"https://www.bbc.co.uk"+link["href"]])
    return headlines

getHeadlines()