#Parameter
movie_id = 'tt1072748' #Choose the movie id you want

import requests
from lxml import etree
url = 'http://www.imdb.com/title/'+movie_id+'/reviews' 
data = requests.get(url).text
s=etree.HTML(data)

film_name=s.xpath('//*[@id="main"]/section/div[1]/div/h3/a/text()')[0]
title=s.xpath('//*[@class="title"]/text()')
date=s.xpath('//*[@class="review-date"]/text()')
content_length=len(s.xpath('//*[@id="main"]/section/div[2]/div[2]/div/div[1]/div[1]/div[@class="content"]'))
content = []
for i in range(content_length):
    temp=s.xpath('//*[@id="main"]/section/div[2]/div[2]/div['+str(i+1)+']/div[1]/div[1]/div[@class="content"]/div[@class="text"]/text()')
    content.append('')
    content[i]='\n'.join(temp).encode("utf8").decode("cp950", "ignore")

print(len(content),len(title),len(date))

review = []
for i in range(content_length):
    temp = {'title':title[i],'date':date[i],'content':content[i]}
    review.append(temp)

my_json = {
    'film name':film_name,
    'review': review
}

#Export to json
import json
parsed=json.dumps(my_json,indent=4, sort_keys=True)
print(parsed)
with open('./output_json/'+film_name+'_review_imdb.json', 'a') as the_file:
  the_file.truncate()
  the_file.write(parsed)
