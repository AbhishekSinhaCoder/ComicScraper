'''
	Taylor King
	telltaylor13@gmail.com
	
	Purpose: Grablinks from a index page of getcomics.info
	Outputs: A link.dat file that contatins a list of links to copy
	for jdownloader




	TODO:
		allow input of a search url and get_link results by page
		Add support for pages like https://getcomics.info/other-comics/sex-criminals-001-010-tpb-free-get_link/

	To run:
		source mods/bin/activate
		python3 comicScraper.py




'''
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path
import os

rawlinks = "links.dat"
set_links = set()




def index_page(url):
	#	Grabs index page
	#	Filters each link to a page
	#	to the appropriate function
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	post_info = soup.findAll('h1',{'class':'post-title'})
	for info in post_info:
		tags = info.findAll('a')
		for tag in tags:
			href_value = tag.get('href')
			#print(href_value)
			if "week" in href_value:
				week_page(href_value)
			else:
				get_link(href_value)


def get_link(url):
	#	Figures out if a page
	#	is a red button or a
	#	collection page passes
	#	a soup to either red or collection
	#	functions

	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	testtag = soup.find('a',{'title':'Download Now'})
	if testtag == None:
		tags = soup.findAll('a',{'rel':'noopener noreferrer'})
		for tag in tags:
			#print(tag)
			span = tag.find('span')
			#print(type(span))
			if span != None:
				if span.text == "Main Server":
					set_links.add(tag.get('href'))
	else:
		set_links.add(testtag.get('href'))



def week_page(url):
	#	New request
	#	New Soup
	#	Grab each link
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.findAll('a',{'rel':'noopener noreferrer'})
	for tag in tags:
		link = tag.get('href')
		if link != None:
			get_link(link)
		else:
			pass




def write_links(linkset):
	with open(rawlinks,"a+") as dataFile:
		for link in linkset:
			dataFile.write(link+'\n')
	



n = 11
#iterates over the newest n pages of comics

base_url = "https://getcomics.info"
query = "/?s=deathstroke"
for i in range(1,n):
	if i == 1:
		
		url = base_url + query
		print(url)
		index_page(url)

	else:
		#Sample url of the home page, 3
		#https://getcomics.info/page/3/
		url = "https://getcomics.info/page/"+str(i)+query
		print(url)
		index_page(url)	
	write_links(set_links)
	set_links.clear()


