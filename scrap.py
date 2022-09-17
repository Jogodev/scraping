import requests
from bs4 import BeautifulSoup
import csv

# CODE POUR UN LIVRE
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')





rating = soup.find('p', class_='star-rating Three').findAll('i')
product_description = soup.find('meta', {'name': 'description'})
category = soup.find('ul', class_='breadcrumb').find('a')
title = soup.find('h1')
image_url = soup.find('img')
tablebook = soup.findAll('td')

with open("books.csv", "w") as book:
    book.write("product_page_url, category, title, product_description, universal_ product_code (upc), price_including_tax, "
               "price_excluding_tax, number_available , review_rating, image_url \n")
    book.write(str(category) + ' , ' + str(title) + ' , ' + str(product_description) + ' , ' + str(tablebook) + ' , ' + str(len(rating)) + ' , ' + str(image_url))

# #url pour une catégorie
# url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
#
# category = soup.findAll('article', class_='product_pod')
# print(category)
# #[print(str(a) + '\n') for a in categs]
# #for li in categs:

