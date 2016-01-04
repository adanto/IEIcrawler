#!/usr/bin/env python

import urllib2
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def extractInfo(url, baseurl, style = []):
	print url

	# Se inicializa el objeto soup para hacer consultas a la url 
	soup = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml')

	# Se obtiene el nombre del concierto. La propiedad (itemprop) que lo contiene es "name"
	festName = soup.find('h1', {'itemprop': 'name'}).getText().strip()

	# El id se consige de la misma forma, en este caso buscando el valor del campo "data-analytics-festival-id"
	festID = soup.find('body')['data-analytics-festival-id'] 

	# La descripcion del festival aparece en la propiedad description, para la cual buscamos todos los paragrafos 
	# (Suele estar dividido en varios), y por ultimo los juntamos con un ' '.join de la lista de paragrafos
	festDesc = soup.find('div', {'itemprop': 'description'}).findAll('p')
	festDesc = ' '.join([p.getText() for p in festDesc])


	# El resultado de los precios puede ser de los siguientes tipos:
	# Sold Out
	# Coming Soon
	# Off Sale
	# Past
	# Valor numerico 
	
	# Si se trata de aguno de los dos primeros, es mas facil.
	validPrices = ['Past', 'Off Sale', 'Sold Out', 'Coming Soon'] 

	statusContainer = soup.find('div', {'class': 'festival-status-container'})
	festPric = statusContainer.find('h3', {'class': 'status'})

	if not festPric.getText().strip() in validPrices:
		# Si no se trata de los validos, se debe buscar en el link el precio de la entrada
		# Cogemos la url base y la extension para acceder a la pagina donde compramos la entrada
		# De aqui si podemos recoger el precio

		ticketLink = statusContainer.find('div', {'class': 'media-icon-icon_tickets'})
		if(ticketLink != None):

			# Tenemos un nuevo link que comprobar para obtener el precio de este festival 
			ticketLink = baseurl[:-1] + ticketLink.find('a').get('href')

			# Abrimos el nuevo link para obtener los precios (Solo queremos el primero lol)
			soupPrices = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml')

			# El data-status es necesario para que no nos liste ofertas ya pasadas
			prices = soupPrices.findAll('div', {'itemprop': 'offers', 'data-status': 'purchasable'})[0]

			# Obtenemos el precio del span y quitamos el signo de euros
			prices = prices.find('span', {'class': 'price'})
			prices = prices.getText().strip()[1:]

			festPric = prices

		else:
			# No hay precios por cualquier otra razon no tenida en cuenta entre las validas
			festPric = 'No price yet'

	else:
		# Recogemos la razon por la que no esta el precio de la entrada
		festPric = festPric.getText().strip()



	# Obtenemos la fecha de inicio del campo startDate 
	festIniData = soup.find('time', {'itemprop': 'startDate'})
	if festIniData != None:
		festIniData = '' if not festIniData.has_attr('datetime') else festIniData['datetime']
	else:
		festIniData = ''


	# Obtenemos la fecha de fin del campo endDate 
	festEndData = soup.find('time', {'itemprop': 'endDate'})
	if festEndData != None:
		festEndData = '' if not festEndData.has_attr('datetime') else festEndData['datetime']
	else:
		festEndData = ''



	# Obtenemos la informacion de posicionamiento de los tags meta latitud y longitud
	latitude = soup.find('meta', {'itemprop': 'longitude'})['content']
	longitude = soup.find('meta', {'itemprop': 'longitude'})['content']

	# La informacion de direccion, ciudad, etc la sacamos del container en cuestion 
	festLocation = soup.find('section', {'id': 'festival-location'}).find('span', {'itemprop': 'address'})

	# Los siguientes tres valores se encuentran uno seguido el uno del otro, cada uno en un span con los siguientes valores de itemprop
	city = festLocation.find('span', {'itemprop': 'addressLocality'})
	if city != None:
		city = city.getText().strip()
	else:
		city = ""
	
	address = festLocation.find('span', {'itemprop': 'streetAddress'})
	if address != None:
		address = address.getText().strip()
	else:
		address = ""


	postalCode = festLocation.find('span', {'itemprop': 'postalCode'})
	if postalCode != None:
		postalCode = postalCode.getText().strip()
	else:
		postalCode = ""

	print city, address, postalCode

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
	url = "http://www.festicket.com/festivals/?page=1"
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
		fest_info = extractInfo(urls[i], main_url, stylesList[i])



		print str((1 + i) * 100.0 / len(urls)) + '%'



if __name__ == "__main__":
	startCrawler()