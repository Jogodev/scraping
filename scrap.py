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
# url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
url = "http://books.toscrape.com/index.html"
response = requests.get()
soup = BeautifulSoup(response.content, 'html.parser')


def click(urls):
    return requests.get(urls)


# def paginate(page_soup):
#     next_button = page_soup.find('li', class_='next').find('a', href=True)
#     if next_button:
#         url_change = url.replace('index.html', str(next_button['href']))
#         next_page = click(url_change)
#         return next_page
#     else:
#         print("Non")
# paginate()

def get_all_books(urls):
    link_books = soup.find('ol', class_='row').findAll('a', href=True)
    for books in link_books:
        link_book = (('http://books.toscrape.com/') + (books['href']))
        book_pages = click(link_book)
        book_soup = BeautifulSoup(book_pages.content, 'html.parser')
        rating = book_soup.find('p', class_='star-rating').findAll('i')
        categ = book_soup.find('li', class_='active').findPrevious('a').text
        title_book = book_soup.find('li', class_='active').text
        product_description = book_soup.find('div', {'id': 'product_description'}).findNext('p').text
        table_book = book_soup.find('table', class_='table table-striped').text
        with open("books.csv", "w") as bookfile:
            bookfile.write(
                "product_page_url ; category ; title ; product_description ; universal_ product_code (upc) ; price_including_tax ; "
                "price_excluding_tax ; number_available  ; review_rating ; image_url \n")
            bookfile.write(str(link_book) + ' ; ' + str(categ) + ' ; ' + str(title_book) + ' ; ' + str(
                product_description) + ' ; ' + str(table_book) + ' ; ' + str(len(rating)))

get_all_books("http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html")
# def scrap():
#     categories = soup.find('div', class_='side_categories').find('ul').find('ul').findAll('a', href=True)
#     for category in categories:
#         category_soup = BeautifulSoup(response.content, 'html.parser')
#         url_change_category = category['href'].replace("..", "")
#         link_category = (('http://books.toscrape.com/') + (url_change_category))
#         category_result = click(link_category)
#         for category_result in category:

