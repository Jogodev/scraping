import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

product_page_url = []
title = []
product_description = []
category = []
review_rating = []
image_url = []
table_book = []

# url = "http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html"
# url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
url = "http://books.toscrape.com/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


def click(url):
    return requests.get(url)


def paginate():
    next_button = soup.find('li', class_='next').find('a', href=True)
    if next_button:
        url_change = url.replace('index.html', str(next_button['href']))
        next_page = requests.get(url_change)
        print(next_page)
    else:
        print("Non")

        
def scrap():
    categories = soup.find('div', class_='side_categories').find('ul').find('ul').findAll('a', href=True)
    books = soup.find('ol', class_='row').findAll('a')
    for category in categories:
        link_category = (('http://books.toscrape.com/') + (category['href']))
        click(link_category)
        for book in books:
            link_books = (('http://books.toscrape.com/') + (book['href']))
            click(link_books)
            print(click(link_books))
            for data in link_books:
                rating = soup.find('p', class_='star-rating Three').findAll('i')
                product_description = soup.find('meta', {'name': 'description'})
                categ = soup.find('li', class_='active')
                title_book = soup.find('h3')
            # with open("books.csv", "w") as bookfile:
            #     bookfile.write(
            #         "product_page_url ; category ; title ; product_description ; universal_ product_code (upc) ; price_including_tax ; "
            #         "price_excluding_tax ; number_available  ; review_rating ; image_url \n")
            #     bookfile.write(str(link_books) + ' ; ' + str(categ) + ' ; ' + str(title_book) + ' ; ' + str(
            #         product_description) + ' ; ' + str(table_book) + ' ; ' + str(len(rating)))


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
