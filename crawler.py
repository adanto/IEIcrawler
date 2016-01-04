#!/usr/bin/env python

import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def extractInfo(url, style = []):



	soup = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml')
	festName = soup.find('h1', {'itemprop': 'name'}).getText().strip()
	festID = soup.find('body')['data-analytics-festival-id'] 
	print festName
	festDesc = soup.find('div', {'itemprop': 'description'}).findAll('p')
	festDesc = ' '.join([p.getText() for p in festDesc])

	# Este resultado puede ser de los siguientes tipos:
	# Sold Out
	# Coming Soon

	validPrices = ['Sold Out', 'Coming Soon'] 

	festPric = soup.find('a', {'class': 'status'})
	if not festPric.getText().strip() in validPrices:
		festPric = soup.find('div', {'class': 'book-package'}).find('a').getText().strip().split()
		# Para que aparezca la moneda -> festPric[4][0]
		festPric = festPric[4][1:]
	else:
		festPric = festPric.getText().strip()



	# festIniData = soup.find('time', {'itemprop': 'startDate'})
	# if festIniData != None:
	# 	festIniData = '' if not festIniData.has_attr('datetime') else festIniData['datetime']
	# else:
	# 	festIniData = ''


	# festEndData = soup.find('time', {'itemprop': 'endDate'})
	# if festEndData != None:
	# 	festEndData = '' if not festEndData.has_attr('datetime') else festEndData['datetime']
	# else:
	# 	festEndData = ''

	# latitude = soup.find('meta', {'itemprop': 'longitude'})['content']
	# longitude = soup.find('meta', {'itemprop': 'longitude'})['content']

	# city = soup.findAll('a', {'href': '#festival-location'})[1].getText().strip()
	
	# address = soup.find('span', {'itemprop': 'streetAddress'}).getText().strip()

	# postalCode = soup.find('span', {'itemprop': 'postalCode'}).getText().strip()

	# lineup = []

	# for artist in soup.findAll('li', {'class': 'artist'}):
	# 	lineup.append(artist.find('span', {'itemprop': 'name'}).getText())

	# return [festName, festID, festDesc, festPric, festIniData, festEndData, latitude, longitude, city, address, postalCode, lineup]
	return []

	


def trade_spider(max_pages, url):
	page = 0
	srcs = []

	while page < max_pages or max_pages == -1 :
		plain_text = urllib2.urlopen(url).read()
		soup = BeautifulSoup(plain_text, 'lxml')
		
		items = soup.find('div', {'class': 'festival-cards'})

		for link in items.findAll('a', {'class': 'button button--big button--secondary button--block'}):
			href = link.get('href')
			srcs.append(href)

		it = 0
		stylesList = []

		for styles in items.findAll('p', {'class': 'music-list'}):
			for i in styles.findAll('span', {'class': 'music-tag'}):
				if len(stylesList) > it:
					stylesList[it].append(i.getText())
				else:
					stylesList.append([i.getText()])
			it += 1

		page += 1 if max_pages != -1 else 0


	return list(set(srcs)), stylesList




def crawler(url, main_url):
	urls = [url]
	crawled_urls = []
	urls_getted = []
	stylesList = []
	crawler_count = 0


	deep = 0
	while deep < 1: 
		for i in urls:
			if i not in crawled_urls:
				if i != None and len(i) > 0:
					if i[0] == '/':
						ancAndStyles = trade_spider(1, main_url + i[1:])
						urls_getted += ancAndStyles[0]
						crawled_urls.append(url + i[1:])
					else:
						if i[0] == '?':
							ancAndStyles = trade_spider(1, url + i)
							urls_getted += ancAndStyles[0]
							crawled_urls.append(main_url + i[1:])
						else:
							if i[0] != '#':
								ancAndStyles = trade_spider(1, i)
								urls_getted += ancAndStyles[0]
								crawled_urls.append(i)

					stylesList = ancAndStyles[1]
					crawler_count += 1
				print crawler_count, "--->", i

		urls += list(set(urls_getted))
		print "crawled_urls", len(crawled_urls), "len(urls_getted)", len(urls_getted), "len(urls)", len(urls) 
		urls_getted = []
		deep += 1
	return urls, stylesList


def startCrawler():
	url = "http://www.festicket.com/festivals/?page=9"
	main_url = "http://www.festicket.com/"
	urls, stylesList = crawler(url, main_url)
	urls = [main_url[:-1] + i for i in urls if i[0] == '/']

	# Preparando XML
	root = ET.Element('catalogoFestivales')
	root.attrib['url'] = main_url
	festivales = ET.SubElement(root, 'festivales')
	ET.dump(root)

	
	for i in xrange(len(urls[:-1])):
		# [festName, festID, festDesc, festPric, festIniData, festEndData, latitude, longitude, city, address, postalCode, lineup]
		fest_info = extractInfo(urls[i], stylesList[i])



		print str((1 + i) * 100.0 / len(urls)) + '%'



if __name__ == "__main__":
	startCrawler()