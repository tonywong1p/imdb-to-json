#Parameter
movie_id = 'tt1072748' #Choose the movie id you want

#General information
import requests
from lxml import etree
url = 'http://www.imdb.com/title/'+movie_id
data = requests.get(url).text
s=etree.HTML(data)

year=s.xpath('//*[@id="titleYear"]/a/text()')[0]
year=int(year)
description=s.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[1]/text()')[0].replace('\n','').strip()
duration=s.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/time/text()')[0].replace('\n','').strip()
genre=s.xpath('//*[@id="titleStoryLine"]/div[3]/a/text()')
for i in range(len(genre)):
    genre[i]=genre[i].strip()
country=s.xpath('//*[@id="titleDetails"]/div[2]/a/text()')[0]
language=s.xpath('//*[@id="titleDetails"]/div[3]/a/text()')[0]
filming_location=s.xpath('//*[@id="titleDetails"]/div[6]/a/text()')[0].split(',')
for i in range(len(filming_location)):
    filming_location[i]=filming_location[i].strip()
box_office_usa_opening_weekend=s.xpath('//*[@id="titleDetails"]/div[7]/text()[2]')[0].replace('\n','').replace('$','').replace(',','').strip()
box_office_usa_opening_weekend=float(box_office_usa_opening_weekend)
box_office_usa=s.xpath('//*[@id="titleDetails"]/div[8]/text()[2]')[0].replace('\n','').replace('$','').replace(',','').strip()
box_office_usa=float(box_office_usa)

#Company Credits
url = 'http://www.imdb.com/title/'+movie_id+'/companycredits' 
data = requests.get(url).text
s=etree.HTML(data)

film_name=s.xpath('//*[@id="main"]/div[1]/div[1]/div/h3/a/text()')[0]
production_company=s.xpath('//*[@id="company_credits_content"]/ul[1]/li/a/text()')
distributor=s.xpath('//*[@id="company_credits_content"]/ul[2]/li/a/text()')

#Full Credits
url = 'http://www.imdb.com/title/'+movie_id+'/fullcredits'
data = requests.get(url).text
s=etree.HTML(data)

director=s.xpath('//*[@id="fullcredits_content"]/table[1]/tbody/tr/td[1]/a/text()')[0].replace('\n','').strip()
writing_credit=s.xpath('//*[@id="fullcredits_content"]/table[2]/tbody/tr/td[1]/a/text()')
for i in range(3):
    writing_credit[i]=writing_credit[i].replace('\n','').strip()
cast=s.xpath('//*[@id="fullcredits_content"]/table[3]/tr/td[2]/a/span/text()')
producer=s.xpath('//*[@id="fullcredits_content"]/table[4]/tbody/tr/td[1]/a/text()')
for i in range(len(producer)):
    producer[i]=producer[i].replace('\n','').strip()

#Release Date
url = 'http://www.imdb.com/title/'+movie_id+'/releaseinfo' 
data = requests.get(url).text
s=etree.HTML(data)

release_location=s.xpath('//*[@id="release_dates"]/tr/td[1]/a/text()')
release_date=s.xpath('//*[@id="release_dates"]/tr/td[2]/text()')

release = []
for i in range(len(release_location)):
    temp = {'location':release_location[i],'date':release_date[i]}
    release.append(temp)

my_json = {
    'film name':film_name,
    'year':year,
    'description':description,
    'duration':duration,
    'genre':genre,
    'country':country,
    'language':language,
    'filming location':filming_location,
    'Opening box office in USA':box_office_usa_opening_weekend,
    'box office in USA':box_office_usa,
    'production company':production_company,
    'distributor':distributor,
    'director':director,
    'writing credit':writing_credit,
    'cast':cast,
    'producer':producer,
    'release':release
}

#Export to json
import json
parsed=json.dumps(my_json,indent=4, sort_keys=True)
print(parsed)
with open('./output_json/'+film_name+'_general_info_imdb.json', 'a') as the_file:
  the_file.truncate()
  the_file.write(parsed)
