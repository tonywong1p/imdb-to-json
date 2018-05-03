#Parameter
movie_id = 'tt1072748' #Choose the movie id you want
max_star_old = 10.0
max_star_new = 5.0
star_rescale = max_star_new/max_star_old

import requests
from lxml import etree
url = 'http://www.imdb.com/title/'+movie_id+'/ratings' 
data = requests.get(url).text
s=etree.HTML(data)

#Film Name
film_name=s.xpath('//*[@itemprop="name"]/a[1]/text()')[0]

#Overall Rating
Overall_Rating_original=s.xpath('//*[@name="ir"]/span[1]/text()')
Overall_Rating=float(Overall_Rating_original[0])*star_rescale
mean_median=s.xpath('//*[@id="main"]/section/div/div[4]/text()')[0].encode("utf8").decode("cp950", "ignore").replace('Arithmetic mean = ','').replace('Median = ',',').replace(' ','').replace('\n','').split(',')
mean=float(mean_median[0])*star_rescale
median=float(mean_median[1])*star_rescale

print(median)

#Rating Quantity from Rating
ratings=s.xpath('//*[@id="main"]/section/div/table[1]/tr/td[3]/div/div/text()')
for i in range(10):
  ratings[i]=int(ratings[i].replace(',',''))
ratings = list(reversed(ratings))
Star_1 = (ratings[0]+ratings[1])/2
Star_2 = (ratings[2]+ratings[3])/2
Star_3 = (ratings[4]+ratings[5])/2
Star_4 = (ratings[6]+ratings[7])/2
Star_5 = (ratings[8]+ratings[9])/2

#Average Rating from diff age group (all,<18,18-29,30-44,45+)
rating_all=s.xpath('//*[@id="main"]/section/div/table[2]/tr[2]/td/div[1]/text()')
rating_male=s.xpath('//*[@id="main"]/section/div/table[2]/tr[3]/td/div[1]/text()')
rating_female=s.xpath('//*[@id="main"]/section/div/table[2]/tr[4]/td/div[1]/text()')
for i in range(5):
  rating_all[i]=float(rating_all[i])
  rating_male[i]=float(rating_male[i])
  rating_female[i]=float(rating_female[i])

#Average Rating from special users (IMDb staff,top 1000 voters, US users, non-US users)
rating_special=s.xpath('//*[@id="main"]/section/div/table[3]/tr[2]/td/div[1]/text()')
for i in range(4):
  rating_special[i]=float(rating_special[i])  

#Rating Quantity from diff age group (all,<18,18-29,30-44,45+)
rating_all_quantity=s.xpath('//*[@id="main"]/section/div/table[2]/tr[2]/td/div[2]/a/text()')
rating_male_quantity=s.xpath('//*[@id="main"]/section/div/table[2]/tr[3]/td/div[2]/a/text()')
rating_female_quantity=s.xpath('//*[@id="main"]/section/div/table[2]/tr[4]/td/div[2]/a/text()')
for i in range(5):
  rating_all_quantity[i]=int(rating_all_quantity[i].replace(' ','').replace('\n','').replace(',',''))
  rating_male_quantity[i]=int(rating_male_quantity[i].replace(' ','').replace('\n','').replace(',',''))
  rating_female_quantity[i]=int(rating_female_quantity[i].replace(' ','').replace('\n','').replace(',',''))

#Rating Quantity from special users (IMDb staff,top 1000 voters, US users, non-US users)
rating_special_quantity=s.xpath('//*[@id="main"]/section/div/table[3]/tr[2]/td/div[2]/a/text()')
for i in range(4):
  rating_special_quantity[i]=int(rating_special_quantity[i].replace(' ','').replace('\n','').replace(',',''))

#Constructing json
my_json = {
  "film name":film_name,
  "overall rating":Overall_Rating,
  "mean":mean,
  "median":median,
  "rating":[
    {"name":"Star 1","quantity":Star_1},
    {"name":"Star 2","quantity":Star_2},
    {"name":"Star 3","quantity":Star_3},
    {"name":"Star 4","quantity":Star_4},
    {"name":"Star 5","quantity":Star_5}
  ],
  "rating_all":[
    {"age":"all ages","avg_rating":rating_all[0],"quantity":rating_all_quantity[0]},
    {"age":"<18","avg_rating":rating_all[1],"quantity":rating_all_quantity[1]},
    {"age":"18-29","avg_rating":rating_all[2],"quantity":rating_all_quantity[2]},
    {"age":"30-44","avg_rating":rating_all[3],"quantity":rating_all_quantity[3]},
    {"age":"45+","avg_rating":rating_all[4],"quantity":rating_all_quantity[4]}
  ],
  "rating_male":[
    {"age":"all ages","avg_rating":rating_male[0],"quantity":rating_male_quantity[0]},
    {"age":"<18","avg_rating":rating_male[1],"quantity":rating_male_quantity[1]},
    {"age":"18-29","avg_rating":rating_male[2],"quantity":rating_male_quantity[2]},
    {"age":"30-44","avg_rating":rating_male[3],"quantity":rating_male_quantity[3]},
    {"age":"45+","avg_rating":rating_male[4],"quantity":rating_male_quantity[4]}
  ],
  "rating_female":[
    {"age":"all ages","avg_rating":rating_female[0],"quantity":rating_female_quantity[0]},
    {"age":"<18","avg_rating":rating_female[1],"quantity":rating_female_quantity[1]},
    {"age":"18-29","avg_rating":rating_female[2],"quantity":rating_female_quantity[2]},
    {"age":"30-44","avg_rating":rating_female[3],"quantity":rating_female_quantity[3]},
    {"age":"45+","avg_rating":rating_female[4],"quantity":rating_female_quantity[4]}
  ],
  "rating_special":[
    {"text":"imdb staff","avg_rating":rating_special[0],"quantity":rating_special_quantity[0]},
    {"text":"top 1000 voters","avg_rating":rating_special[1],"quantity":rating_special_quantity[1]},
    {"text":"US users","avg_rating":rating_special[2],"quantity":rating_special_quantity[2]},
    {"text":"non-US users","avg_rating":rating_special[3],"quantity":rating_special_quantity[3]}
  ]
}

#Export to json
import json
parsed=json.dumps(my_json,indent=4, sort_keys=True)
print(parsed)
with open('./output_json/'+film_name+'_rating_imdb.json', 'a') as the_file:
  the_file.truncate()
  the_file.write(parsed)
