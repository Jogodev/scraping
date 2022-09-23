import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# CODE POUR UN LIVRE

product_page_url = []
title = []
product_description = []
category = []
review_rating = []
image_url = []
table_book = []

url = "http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


def paginate():
    page_number = soup.find('li', class_='next').find('a', href=True)
    url_change = url.replace('index.html', page_number['href'])
    next_page = requests.get(url_change)

def scrap():

    for book in urls:
        #requests.get(urls)
        product_page_url = soup.find('h3').find('a')
        rating = soup.find('p', class_='star-rating Three').findAll('i')
        product_description = soup.find('meta', {'name': 'description'}).text
        category = soup.find('li', class_='active').text
        title_book = soup.find('h3').text
        table_book = soup.findAll('td')
        print(urls)
        with open("books.csv", "w") as books:
            books.write(
                "product_page_url ; category ; title ; product_description ; universal_ product_code (upc) ; price_including_tax ; "
                "price_excluding_tax ; number_available  ; review_rating ; image_url \n")
            books.write(str(product_page_url) + ' ; ' + str(category) + ' ; ' + str(title_book) + ' ; ' + str(
                product_description) + ' ; ' + str(table_book) + ' ; ' + str(len(rating)))


scrap()
# #url pour une catégorie
# url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
#
# category = soup.findAll('article', class_='product_pod')
# print(category)
# #[print(str(a) + '\n') for a in categs]
# #for li in categs:
# soup = BeautifulSoup(html)
#
# for a in soup.find_all('a', href=True):
#     print("Found the URL:", a['href'])
